from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
from .parser import StatementRow
from .normalizer import normalize_statement_rows, infer_financial_metrics, NormalizedMetrics


@dataclass(frozen=True)
class AccountingSnapshot:
    company_cvm_code: str | None
    company_name: str | None
    document_type: str
    reference_period: str | None
    disclosure_date: str | None
    version: int
    net_income: float | None
    attributable_net_income: float | None
    equity_attributable_common: float | None
    cash_and_equivalents: float | None
    financial_debt: float | None
    net_debt: float | None
    ebitda: float | None
    debt_ebitda: float | None
    quality_flags: tuple[str, ...]
    evidence: dict[str, tuple[str, ...]]


def build_accounting_snapshots(rows: Iterable[StatementRow]) -> list[AccountingSnapshot]:
    rows = list(rows)
    normalized = normalize_statement_rows(rows)
    out: list[AccountingSnapshot] = []
    for m in normalized:
        group = [r for r in rows if (r.company_cvm_code, r.reference_period, r.version) ==
                 (m.company_cvm_code, m.reference_period, m.version)]
        company_name = next((r.company_name for r in group if r.company_name), None)
        document_type = next((r.document_type for r in group if r.document_type), "UNKNOWN")
        inferred = infer_financial_metrics(m)
        evidence = {k: tuple(v) for k, v in (m.evidence or {}).items()}
        out.append(AccountingSnapshot(
            company_cvm_code=m.company_cvm_code,
            company_name=company_name,
            document_type=document_type,
            reference_period=m.reference_period,
            disclosure_date=m.disclosure_date,
            version=m.version,
            net_income=m.net_income,
            attributable_net_income=m.attributable_net_income,
            equity_attributable_common=m.equity_attributable_common,
            cash_and_equivalents=m.cash_and_equivalents,
            financial_debt=m.financial_debt,
            net_debt=inferred["net_debt"],
            ebitda=m.ebitda,
            debt_ebitda=inferred["debt_ebitda"],
            quality_flags=tuple(m.quality_flags or ()),
            evidence=evidence,
        ))
    return out


def select_latest_snapshot(snapshots: Iterable[AccountingSnapshot]) -> AccountingSnapshot | None:
    items = list(snapshots)
    if not items:
        return None
    # Re-presentations must win over the older version for the same period.
    return max(items, key=lambda x: (x.reference_period or "", x.version, x.disclosure_date or ""))
