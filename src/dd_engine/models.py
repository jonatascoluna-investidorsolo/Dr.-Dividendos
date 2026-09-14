from dataclasses import dataclass
from typing import Optional


@dataclass
class CompanyInput:
    ticker: str
    company_name: str
    sector: Optional[str] = None
    is_financial: bool = False
    shares: Optional[float] = None
    projected_net_income: Optional[float] = None
    book_value_per_share: Optional[float] = None
    net_debt_ebitda: Optional[float] = None
    earnings_cagr_5y: Optional[float] = None
    payout_expected: Optional[float] = None
    current_price: Optional[float] = None
    historical_pe_10y: Optional[float] = None


@dataclass
class CalculationResult:
    lpa: Optional[float]
    dpa: Optional[float]
    dividend_yield: Optional[float]
    pe_current: Optional[float]
    pb_current: Optional[float]
    graham_value: Optional[float]
    graham_upside: Optional[float]
    bazin_ceiling: Optional[float]
    bazin_margin: Optional[float]
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
