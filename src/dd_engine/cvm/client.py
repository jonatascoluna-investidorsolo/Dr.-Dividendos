from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import time

@dataclass(frozen=True)
class CVMEndpoints:
    base: str = "https://dados.cvm.gov.br/dados/CIA_ABERTA"

    def dfp_zip(self, year: int) -> str:
        return f"{self.base}/DOC/DFP/DADOS/dfp_cia_aberta_{year}.zip"

    def itr_zip(self, year: int) -> str:
        return f"{self.base}/DOC/ITR/DADOS/itr_cia_aberta_{year}.zip"

    def cadastro_csv(self) -> str:
        return f"{self.base}/CAD/DADOS/cad_cia_aberta.csv"

    def fca_zip(self, year: int) -> str:
        return f"{self.base}/DOC/FCA/DADOS/fca_cia_aberta_{year}.zip"

class CVMClient:
    """Small dependency-free downloader for official CVM open-data archives."""
    def __init__(self, endpoints: CVMEndpoints | None = None, user_agent: str = "DoutorDosDividendos/0.4"):
        self.endpoints = endpoints or CVMEndpoints()
        self.user_agent = user_agent

    def download(self, url: str, destination: str | Path, timeout: int = 60, retries: int = 3) -> Path:
        dest = Path(destination)
        dest.parent.mkdir(parents=True, exist_ok=True)
        last_error = None
        for attempt in range(1, retries + 1):
            try:
                req = Request(url, headers={"User-Agent": self.user_agent})
                with urlopen(req, timeout=timeout) as response, dest.open("wb") as fh:
                    fh.write(response.read())
                return dest
            except (URLError, HTTPError) as exc:
                last_error = exc
                if attempt < retries:
                    time.sleep(attempt * 2)
        raise RuntimeError(f"Falha ao baixar fonte CVM após {retries} tentativas: {url}") from last_error

    def use_local_archive(self, source: str | Path, destination: str | Path) -> Path:
        source, destination = Path(source), Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())
        return destination

    def download_dfp(self, year: int, destination: str | Path) -> Path:
        return self.download(self.endpoints.dfp_zip(year), destination)

    def download_itr(self, year: int, destination: str | Path) -> Path:
        return self.download(self.endpoints.itr_zip(year), destination)

    def download_cadastro(self, destination: str | Path) -> Path:
        return self.download(self.endpoints.cadastro_csv(), destination)

    def download_fca(self, year: int, destination: str | Path) -> Path:
        return self.download(self.endpoints.fca_zip(year), destination)
