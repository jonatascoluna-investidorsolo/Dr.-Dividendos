from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from math import prod
from typing import Iterable


@dataclass(frozen=True)
class ShareCountPoint:
    period: str
    shares: float
    source: str = "CVM"
    class_code: str | None = None


@dataclass(frozen=True)
class ShareAdjustment:
    effective_date: date
    factor: float
    action_type: str
    source_event_id: str | None = None
    status: str = "VALID"

    def __post_init__(self) -> None:
        if self.factor <= 0:
            raise ValueError("share adjustment factor must be > 0")


def adjusted_share_count(
    reported_shares: float,
    period_end: date,
    adjustments: Iterable[ShareAdjustment],
    as_of: date | None = None,
) -> float:
    """Restate historical shares onto the as-of share basis.

    Only valid actions occurring after the historical period and on/before as_of
    are applied. A 2:1 split has factor 2; a 1:2 reverse split has factor 0.5.
    """
    if reported_shares <= 0:
        raise ValueError("reported_shares must be > 0")
    cutoff = as_of or date.max
    factors = [
        a.factor for a in adjustments
        if a.status == "VALID" and period_end < a.effective_date <= cutoff
    ]
    return reported_shares * prod(factors)


def split_factor(new_shares: float, old_shares: float) -> float:
    if new_shares <= 0 or old_shares <= 0:
        raise ValueError("share quantities must be > 0")
    return new_shares / old_shares
