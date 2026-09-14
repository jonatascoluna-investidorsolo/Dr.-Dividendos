from dataclasses import dataclass


@dataclass(frozen=True)
class MethodologyParameters:
    bazin_min_yield: float = 0.06
    gordon_required_return: float = 0.12
    max_growth: float = 0.06
    max_net_debt_ebitda: float = 3.0
    projection_years: int = 5
    projective_required_yield: float = 0.07
    max_healthy_payout: float = 0.80
    min_margin_of_safety: float = 0.20
    event_lookahead_days: int = 45
