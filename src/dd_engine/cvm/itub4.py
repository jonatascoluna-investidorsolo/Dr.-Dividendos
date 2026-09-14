from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .client import CVMClient
from .parser import CVMTableParser, StatementRow
from .canonical import build_accounting_snapshots, AccountingSnapshot
from .periods import select_latest_annual


@dataclass(frozen=True)
class ITUB4RunResult:
    ticker: str
    cvm_code: str
    dfp_path: str
    itr_path: str
    annual_period: str | None
    normalized_rows: int
    status: str
    warnings: tuple[str, ...]


def filter_cvm_code(rows: Iterable[StatementRow], cvm_code: str) -> list[StatementRow]:
    return [r for r in rows if str(r.company_cvm_code or "") == str(cvm_code)]


def build_itub4_snapshot(
    dfp_zip: str | Path,
    cvm_code: str,
) -> tuple[AccountingSnapshot | None, list[AccountingSnapshot]]:
    parser = CVMTableParser()
    rows = filter_cvm_code(parser.parse_zip(dfp_zip, "DFP"), cvm_code)
    snapshots = build_accounting_snapshots(rows)
    annual = select_latest_annual(snapshots)
    return annual, snapshots


def prepare_itub4(
    year: int,
    output_dir: str | Path,
    cvm_code: str,
    client: CVMClient | None = None,
) -> ITUB4RunResult:
    client = client or CVMClient(user_agent="DoutorDosDividendos/2.4")
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    dfp = out / f"dfp_itub4_{year}.zip"
    itr = out / f"itr_itub4_{year}.zip"
    client.download_dfp(year, dfp)
    client.download_itr(year, itr)
    annual, normalized = build_itub4_snapshot(dfp, cvm_code)
    warnings: list[str] = []
    if annual is None:
        warnings.append("DFP_ANNUAL_SNAPSHOT_NOT_FOUND")
    return ITUB4RunResult(
        ticker="ITUB4",
        cvm_code=str(cvm_code),
        dfp_path=str(dfp),
        itr_path=str(itr),
        annual_period=annual.reference_period if annual else None,
        normalized_rows=len(normalized),
        status="REVIEW" if warnings else "READY",
        warnings=tuple(warnings),
    )
