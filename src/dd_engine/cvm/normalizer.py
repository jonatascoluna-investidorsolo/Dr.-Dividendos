from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict
from typing import Iterable
from .parser import StatementRow
from .account_mappings import MAPPINGS

@dataclass
class NormalizedMetrics:
    company_cvm_code: str | None
    reference_period: str | None
    disclosure_date: str | None
    version: int
    net_income: float | None = None
    attributable_net_income: float | None = None
    equity_attributable_common: float | None = None
    cash_and_equivalents: float | None = None
    financial_debt: float | None = None
    ebitda: float | None = None
    shares_outstanding: float | None = None
    evidence: dict[str, list[str]] | None = None
    quality_flags: list[str] | None = None


def _norm(s: str | None) -> str:
    return " ".join((s or "").casefold().strip().split())


def _statement_base(statement: str | None) -> str:
    s = (statement or "").upper()
    for base in ("DRE", "BPA", "BPP"):
        if base in s:
            return base
    return s


def _matches(row: StatementRow, mapping) -> bool:
    if _statement_base(row.statement) != mapping.statement:
        return False
    name = _norm(row.account_name)
    if mapping.account_code and (row.account_code or "") != mapping.account_code:
        return False
    return any(_norm(p) in name for p in mapping.name_contains)


def _choose(rows: list[StatementRow], mapping):
    candidates = [r for r in rows if r.value is not None and _matches(r, mapping)]
    candidates.sort(key=lambda r: (mapping.priority, len(_norm(r.account_name)), r.account_code or ""))
    return candidates[0] if candidates else None


def normalize_statement_rows(rows: Iterable[StatementRow]) -> list[NormalizedMetrics]:
    groups = defaultdict(list)
    for row in rows:
        key = (row.company_cvm_code, row.reference_period, row.version)
        groups[key].append(row)

    result = []
    for (cvm_code, period, version), group in groups.items():
        m = NormalizedMetrics(
            cvm_code, period,
            next((r.disclosure_date for r in group if r.disclosure_date), None),
            version, evidence=defaultdict(list), quality_flags=[]
        )

        selected: dict[str, StatementRow] = {}
        for mapping in MAPPINGS:
            if mapping.metric in selected:
                continue
            candidate = _choose(group, mapping)
            if candidate is not None:
                selected[mapping.metric] = candidate
                setattr(m, mapping.metric, candidate.value * mapping.sign)
                m.evidence[mapping.metric].append(
                    f"{candidate.statement}:{candidate.account_code}:{candidate.account_name}:{candidate.exercise_order}"
                )

        # Debt is deliberately NOT the sum of all matching rows: parent rows
        # can contain the child rows. Prefer the explicit short+long pair, and
        # fall back to one total line only if a pair is unavailable.
        short = selected.get("short_debt")
        long = selected.get("long_debt")
        total = selected.get("total_debt")
        if short is not None and long is not None:
            m.financial_debt = short.value + long.value
        elif total is not None:
            m.financial_debt = total.value
        elif short is not None:
            m.financial_debt = short.value
        elif long is not None:
            m.financial_debt = long.value

        if m.attributable_net_income is None and m.net_income is not None:
            m.quality_flags.append("attributable_net_income_not_found_using_net_income")

        result.append(m)
    return result


def infer_financial_metrics(normalized: NormalizedMetrics) -> dict[str, float | None]:
    net_debt = None
    if normalized.financial_debt is not None and normalized.cash_and_equivalents is not None:
        net_debt = normalized.financial_debt - normalized.cash_and_equivalents
    debt_ebitda = None
    if net_debt is not None and normalized.ebitda and normalized.ebitda > 0:
        debt_ebitda = net_debt / normalized.ebitda
    return {"net_debt": net_debt, "debt_ebitda": debt_ebitda}
