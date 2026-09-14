from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Iterable, Optional

from .shares import ShareAdjustment, adjusted_share_count


@dataclass(frozen=True)
class HistoricalAccountingPoint:
    period: str
    period_end: date
    attributable_net_income: Optional[float]
    equity_attributable_common: Optional[float]
    reported_shares: Optional[float]


@dataclass(frozen=True)
class HistoricalFundamentalPoint:
    period: str
    period_end: date
    adjusted_shares: Optional[float]
    lpa: Optional[float]
    vpa: Optional[float]
    quality_flags: tuple[str, ...] = ()


def build_historical_fundamentals(
    points: Iterable[HistoricalAccountingPoint],
    adjustments: Iterable[ShareAdjustment],
    as_of: date | None = None,
) -> list[HistoricalFundamentalPoint]:
    actions = tuple(adjustments)
    result: list[HistoricalFundamentalPoint] = []
    for p in sorted(points, key=lambda x: x.period):
        flags: list[str] = []
        shares = None
        if p.reported_shares is not None and p.reported_shares > 0:
            shares = adjusted_share_count(p.reported_shares, p.period_end, actions, as_of)
        else:
            flags.append("historical_shares_missing")

        lpa = None
        if p.attributable_net_income is not None and shares:
            lpa = p.attributable_net_income / shares
        elif p.attributable_net_income is not None:
            flags.append("historical_lpa_unavailable")

        vpa = None
        if p.equity_attributable_common is not None and shares:
            vpa = p.equity_attributable_common / shares
        elif p.equity_attributable_common is not None:
            flags.append("historical_vpa_unavailable")

        result.append(HistoricalFundamentalPoint(
            period=p.period,
            period_end=p.period_end,
            adjusted_shares=shares,
            lpa=lpa,
            vpa=vpa,
            quality_flags=tuple(flags),
        ))
    return result
