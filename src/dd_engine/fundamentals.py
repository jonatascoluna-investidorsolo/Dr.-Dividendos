from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Sequence

from .calculations import (
    applied_growth, bazin_ceiling, bazin_margin, current_pb, current_pe,
    dpa, dividend_yield, graham_value, gordon_value, projective_ceiling,
    projected_dpa, projected_lpa, score_debt, score_dividend_yield,
    score_growth, score_margin, score_payout, seal, upside,
)
from .cvm.canonical import AccountingSnapshot


@dataclass(frozen=True)
class HistoricalPoint:
    period: str
    attributable_net_income: Optional[float]


@dataclass(frozen=True)
class FundamentalInput:
    snapshot: AccountingSnapshot
    shares: Optional[float]
    price: Optional[float]
    payout: Optional[float]
    historical: Sequence[HistoricalPoint] = ()
    financial_institution: bool = False
    min_yield: float = 0.06
    required_return: float = 0.12
    max_growth: float = 0.06
    projection_years: int = 5
    projective_yield: float = 0.07
    healthy_payout: float = 0.80
    max_debt_ebitda: float = 3.0


@dataclass(frozen=True)
class FundamentalMetrics:
    lpa: Optional[float]
    vpa: Optional[float]
    dpa: Optional[float]
    dividend_yield: Optional[float]
    pe_current: Optional[float]
    pb_current: Optional[float]
    graham_value: Optional[float]
    graham_upside: Optional[float]
    bazin_ceiling: Optional[float]
    bazin_margin: Optional[float]
    cagr_5y: Optional[float]
    applied_growth: Optional[float]
    gordon_value: Optional[float]
    gordon_upside: Optional[float]
    projected_lpa: Optional[float]
    projected_dpa: Optional[float]
    projective_ceiling: Optional[float]
    projective_upside: Optional[float]
    dy_score: float
    margin_score: float
    debt_score: float
    growth_score: float
    payout_score: float
    quality_score: float
    seal: str
    flags: tuple[str, ...]


def earnings_cagr_5y(points: Sequence[HistoricalPoint]) -> Optional[float]:
    valid = [p for p in points if p.attributable_net_income is not None and p.attributable_net_income > 0]
    if len(valid) < 2:
        return None
    valid = sorted(valid, key=lambda p: p.period)
    first, last = valid[0], valid[-1]
    # Require an actual five-year interval; otherwise do not manufacture a CAGR.
    from datetime import date
    try:
        y0, y1 = int(first.period[:4]), int(last.period[:4])
    except (ValueError, TypeError):
        return None
    if y1 - y0 != 5 or first.attributable_net_income is None or last.attributable_net_income is None:
        return None
    return (last.attributable_net_income / first.attributable_net_income) ** (1 / 5) - 1


def calculate_fundamentals(inp: FundamentalInput) -> FundamentalMetrics:
    s = inp.snapshot
    flags = list(s.quality_flags)
    earnings = s.attributable_net_income if s.attributable_net_income is not None else s.net_income
    lpa_v = earnings / inp.shares if earnings is not None and inp.shares and inp.shares > 0 else None
    vpa_v = s.equity_attributable_common / inp.shares if s.equity_attributable_common is not None and inp.shares and inp.shares > 0 else None
    if inp.shares is None or inp.shares <= 0:
        flags.append("shares_required_for_lpa_vpa")
    if inp.financial_institution:
        flags.append("financial_institution_debt_ebitda_not_applicable")
    cagr = earnings_cagr_5y(inp.historical)
    g = applied_growth(cagr, inp.max_growth)
    dpa_v = dpa(lpa_v, inp.payout)
    dy = dividend_yield(dpa_v, inp.price)
    pe = current_pe(inp.price, lpa_v)
    pb = current_pb(inp.price, vpa_v)
    graham = graham_value(lpa_v, vpa_v)
    bazin = bazin_ceiling(dpa_v, inp.min_yield)
    margin = bazin_margin(inp.price, bazin)
    gordon = gordon_value(dpa_v, g, inp.required_return)
    plpa = projected_lpa(lpa_v, g, inp.projection_years)
    pdpa = projected_dpa(plpa, inp.payout)
    pceiling = projective_ceiling(pdpa, inp.projective_yield)
    debt_score = score_debt(None if inp.financial_institution else s.debt_ebitda, inp.max_debt_ebitda, inp.financial_institution)
    scores = (
        score_dividend_yield(dy, inp.min_yield), score_margin(margin), debt_score,
        score_growth(cagr), score_payout(inp.payout, inp.healthy_payout)
    )
    total = round(sum(scores))
    return FundamentalMetrics(
        lpa_v, vpa_v, dpa_v, dy, pe, pb, graham, upside(graham, inp.price), bazin, margin,
        cagr, g, gordon, upside(gordon, inp.price), plpa, pdpa, pceiling, upside(pceiling, inp.price),
        *scores, float(total), seal(total), tuple(dict.fromkeys(flags))
    )
