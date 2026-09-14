from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import csv
from typing import Iterable

from .cvm.fca import TickerMapping
from .cvm.universe import UniverseItem

@dataclass(frozen=True)
class UniverseValidation:
    ticker: str
    excel_company: str
    cvm_company: str | None
    cvm_code: str | None
    cnpj: str | None
    likely_bdr: bool
    status: str
    reason: str


def validate_universe(items: Iterable[UniverseItem], mappings: Iterable[TickerMapping]) -> list[UniverseValidation]:
    by_ticker: dict[str, list[TickerMapping]] = {}
    for m in mappings:
        by_ticker.setdefault(m.ticker.upper().strip(), []).append(m)
    out: list[UniverseValidation] = []
    for item in items:
        candidates = by_ticker.get(item.ticker.upper(), [])
        if item.likely_bdr and not candidates:
            status, reason = "SPECIAL_HANDLING", "Ticker com padrão provável de BDR; não inferir emissor CVM."
            cvm_company = cvm_code = cnpj = None
        elif len(candidates) == 1:
            m = candidates[0]
            status, reason = "MATCH", "Ticker mapeado univocamente no FCA."
            cvm_company, cvm_code, cnpj = m.company_name, m.cvm_code, m.cnpj
        elif len(candidates) > 1:
            status, reason = "REVIEW", "Mais de um registro FCA para o ticker; requer desambiguação temporal."
            cvm_company = candidates[0].company_name
            cvm_code = candidates[0].cvm_code
            cnpj = candidates[0].cnpj
        else:
            status, reason = "MISSING", "Ticker não localizado no FCA fornecido."
            cvm_company = cvm_code = cnpj = None
        out.append(UniverseValidation(item.ticker, item.company_name, cvm_company, cvm_code, cnpj, item.likely_bdr, status, reason))
    return out


def write_validation_csv(rows: Iterable[UniverseValidation], path: str | Path) -> None:
    rows = list(rows)
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(rows[0]).keys()) if rows else ["ticker"])
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))
