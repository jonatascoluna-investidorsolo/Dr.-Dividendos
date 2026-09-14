from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Iterable, Optional

from .canonical import AccountingSnapshot


@dataclass(frozen=True)
class PeriodSelection:
    reference_period: str
    document_type: str
    version: int
    disclosure_date: Optional[str]
    snapshot: AccountingSnapshot
    selection_reason: str


def _period_key(s: AccountingSnapshot) -> tuple[str, int, str]:
    return (s.reference_period or "", s.version, s.disclosure_date or "")


def latest_by_reference_period(snapshots: Iterable[AccountingSnapshot]) -> list[AccountingSnapshot]:
    """Keep the highest disclosed version for each company/reference period.

    This is the first layer of restatement handling: a later version replaces an
    earlier version for the same reference period, while older periods remain
    available for historical calculations.
    """
    chosen: dict[tuple[str | None, str | None], AccountingSnapshot] = {}
    for snap in snapshots:
        key = (snap.company_cvm_code, snap.reference_period)
        old = chosen.get(key)
        if old is None or _period_key(snap) > _period_key(old):
            chosen[key] = snap
    return sorted(chosen.values(), key=lambda x: (x.reference_period or "", x.disclosure_date or ""))


def select_latest_annual(snapshots: Iterable[AccountingSnapshot]) -> AccountingSnapshot | None:
    """Select the latest DFP snapshot, preferring the most recent reference year."""
    annual = [s for s in latest_by_reference_period(snapshots) if s.document_type.upper() == "DFP"]
    if not annual:
        return None
    return max(annual, key=lambda s: (s.reference_period or "", s.disclosure_date or ""))


def build_historical_annual_series(snapshots: Iterable[AccountingSnapshot]) -> list[AccountingSnapshot]:
    """Return one validated/restatement-resolved DFP snapshot per reference period."""
    annual = [s for s in latest_by_reference_period(snapshots) if s.document_type.upper() == "DFP"]
    return annual
