from __future__ import annotations

import math
from statistics import median
from typing import Iterable, Optional

from .settings import MethodologyParameters


def safe_div(a: Optional[float], b: Optional[float]) -> Optional[float]:
    if a is None or b is None or b == 0:
        return None
    return a / b


def lpa(projected_net_income: Optional[float], shares: Optional[float]) -> Optional[float]:
    return safe_div(projected_net_income, shares)


def dpa(lpa_value: Optional[float], payout: Optional[float]) -> Optional[float]:
    if lpa_value is None or payout is None:
        return None
    return lpa_value * payout


def dividend_yield(dpa_value: Optional[float], price: Optional[float]) -> Optional[float]:
    return safe_div(dpa_value, price)


def current_pe(price: Optional[float], lpa_value: Optional[float]) -> Optional[float]:
    if price is None or lpa_value is None or lpa_value <= 0:
        return None
    return price / lpa_value


def current_pb(price: Optional[float], book_value_per_share: Optional[float]) -> Optional[float]:
    if price is None or book_value_per_share is None or book_value_per_share <= 0:
        return None
    return price / book_value_per_share


def graham_value(lpa_value: Optional[float], vpa: Optional[float]) -> Optional[float]:
    if lpa_value is None or vpa is None or lpa_value <= 0 or vpa <= 0:
        return None
    return math.sqrt(22.5 * lpa_value * vpa)


def upside(target: Optional[float], price: Optional[float]) -> Optional[float]:
    if target is None or price is None or price == 0:
        return None
    return target / price - 1


def bazin_ceiling(dpa_value: Optional[float], minimum_yield: float) -> Optional[float]:
    if dpa_value is None or dpa_value <= 0 or minimum_yield <= 0:
        return None
    return dpa_value / minimum_yield


def bazin_margin(price: Optional[float], ceiling: Optional[float]) -> Optional[float]:
    if price is None or ceiling is None or ceiling == 0:
        return None
    return 1 - price / ceiling


def applied_growth(earnings_cagr_5y: Optional[float], max_growth: float) -> Optional[float]:
    if earnings_cagr_5y is None:
        return None
    return min(max(earnings_cagr_5y, 0), max_growth)


def gordon_value(dpa_value: Optional[float], growth: Optional[float], required_return: float) -> Optional[float]:
    if dpa_value is None or dpa_value <= 0 or growth is None or required_return <= growth:
        return None
    return dpa_value * (1 + growth) / (required_return - growth)


def projected_lpa(lpa_value: Optional[float], growth: Optional[float], years: int) -> Optional[float]:
    if lpa_value is None or growth is None or years < 0:
        return None
    return lpa_value * (1 + growth) ** years


def projected_dpa(projected_lpa_value: Optional[float], payout: Optional[float]) -> Optional[float]:
    return dpa(projected_lpa_value, payout)


def projective_ceiling(projected_dpa_value: Optional[float], required_yield: float) -> Optional[float]:
    if projected_dpa_value is None or projected_dpa_value <= 0 or required_yield <= 0:
        return None
    return projected_dpa_value / required_yield


def score_dividend_yield(dy: Optional[float], minimum_yield: float) -> float:
    if dy is None or minimum_yield <= 0:
        return 0.0
    return min(25.0, max(0.0, dy / minimum_yield * 25.0))


def score_margin(margin: Optional[float]) -> float:
    if margin is None:
        return 0.0
    return min(25.0, max(0.0, margin * 100))


def score_debt(net_debt_ebitda: Optional[float], max_debt: float, is_financial: bool = False) -> float:
    if is_financial:
        return 0.0
    if net_debt_ebitda is None:
        return 0.0
    if net_debt_ebitda < 0:
        return 20.0
    if net_debt_ebitda == 0:
        return 14.0
    return max(0.0, 20.0 * (1 - net_debt_ebitda / max_debt)) if max_debt > 0 else 0.0


def score_growth(cagr: Optional[float]) -> float:
    if cagr is None:
        return 0.0
    return min(15.0, max(0.0, cagr * 100))


def score_payout(payout: Optional[float], healthy_limit: float) -> float:
    if payout is None or payout <= 0:
        return 0.0
    if payout <= healthy_limit:
        return 15.0
    return max(0.0, 15.0 * (1 - (payout - healthy_limit) / 0.5))


def excel_round(value: float) -> int:
    """Round like Excel ROUND(value, 0): halves away from zero."""
    if value >= 0:
        return math.floor(value + 0.5)
    return math.ceil(value - 0.5)


def seal(score: float) -> str:
    if score >= 70:
        return "VERDE"
    if score >= 50:
        return "AMARELO"
    return "VERMELHO"


def median_valid(values: Iterable[Optional[float]]) -> Optional[float]:
    valid = [v for v in values if v is not None and math.isfinite(v)]
    return median(valid) if valid else None
