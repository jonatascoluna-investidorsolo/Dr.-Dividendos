from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen

CVM_DFP = "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/dfp_cia_aberta_{year}.zip"
CVM_ITR = "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/itr_cia_aberta_{year}.zip"

@dataclass(frozen=True)
class AcquisitionResult:
    source: str
    url: str
    path: str | None
    status: str
    sha256: str | None
    collected_at: str
    error: str | None = None


def sha256_file(path: Path) -> str:
    h = sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, dest: Path, *, timeout: int = 30, user_agent: str = "DoutorDosDividendos/0.6") -> AcquisitionResult:
    dest.parent.mkdir(parents=True, exist_ok=True)
    collected = datetime.now(timezone.utc).isoformat()
    try:
        req = Request(url, headers={"User-Agent": user_agent, "Accept": "application/zip,*/*"})
        with urlopen(req, timeout=timeout) as r, dest.open("wb") as out:
            while True:
                chunk = r.read(1024 * 1024)
                if not chunk:
                    break
                out.write(chunk)
        digest = sha256_file(dest)
        return AcquisitionResult("CVM", url, str(dest), "DOWNLOADED", digest, collected)
    except Exception as exc:
        if dest.exists() and dest.stat().st_size == 0:
            dest.unlink()
        return AcquisitionResult("CVM", url, None, "UNREACHABLE", None, collected, repr(exc))


def build_manifest(year: int, root: Path) -> list[AcquisitionResult]:
    specs = [
        ("DFP", CVM_DFP.format(year=year), root / f"dfp_cia_aberta_{year}.zip"),
        ("ITR", CVM_ITR.format(year=year), root / f"itr_cia_aberta_{year}.zip"),
    ]
    results = []
    for source, url, dest in specs:
        r = download(url, dest)
        results.append(AcquisitionResult(source, r.url, r.path, r.status, r.sha256, r.collected_at, r.error))
    return results
