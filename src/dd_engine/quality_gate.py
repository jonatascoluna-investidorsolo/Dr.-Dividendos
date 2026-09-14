from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class QualityGateResult:
    status: str
    ranking_eligible: bool
    score: int
    critical_flags: tuple[str, ...]
    warnings: tuple[str, ...]


def evaluate_quality_gate(company: dict[str, Any]) -> QualityGateResult:
    """Conservative gate for displaying/ranking a company.

    APPROVED means identity + quote + core accounting inputs are coherent enough
    for the calculated metrics. REVIEW means the company can be shown but should
    not enter the main ranking. BLOCKED means identity/data integrity is missing.
    """
    critical: list[str] = []
    warnings: list[str] = []
    score = 100

    if not company.get("ticker") or not company.get("company_name"):
        critical.append("IDENTITY_MISSING")
    if company.get("last_data_quality_status") in {"SOURCE_UNREACHABLE", "BLOCKED"}:
        critical.append("SOURCE_UNAVAILABLE")

    m = company.get("latest_metrics") or {}
    price = m.get("close", m.get("current_price"))
    lpa = m.get("lpa")
    vpa = m.get("vpa")
    dpa = m.get("dpa")

    if price is None or price <= 0:
        critical.append("QUOTE_MISSING")
    if lpa is None:
        critical.append("LPA_MISSING")
    if vpa is None:
        warnings.append("VPA_MISSING")
    if dpa is None:
        warnings.append("DPA_MISSING")

    if not m:
        critical.append("CALCULATION_MISSING")

    if critical:
        return QualityGateResult("BLOCKED", False, 0, tuple(critical), tuple(warnings))

    if vpa is None:
        score -= 25
    if dpa is None:
        score -= 15
    if company.get("last_data_quality_status") not in {None, "READY"}:
        score -= 20
        warnings.append("DATA_STATUS_REVIEW")

    if score >= 80 and not warnings:
        return QualityGateResult("APPROVED", True, score, tuple(), tuple())
    return QualityGateResult("REVIEW", False, max(score, 0), tuple(), tuple(dict.fromkeys(warnings)))
