from .calculations import *
from .models import CalculationResult, CompanyInput
from .settings import MethodologyParameters


def calculate_company(company: CompanyInput, p: MethodologyParameters = MethodologyParameters()) -> CalculationResult:
    lpa_v = lpa(company.projected_net_income, company.shares)
    dpa_v = dpa(lpa_v, company.payout_expected)
    dy_v = dividend_yield(dpa_v, company.current_price)
    pe_v = current_pe(company.current_price, lpa_v)
    pb_v = current_pb(company.current_price, company.book_value_per_share)

    graham_v = graham_value(lpa_v, company.book_value_per_share)
    graham_u = upside(graham_v, company.current_price)
    bazin_v = bazin_ceiling(dpa_v, p.bazin_min_yield)
    bazin_m = bazin_margin(company.current_price, bazin_v)
    growth_v = applied_growth(company.earnings_cagr_5y, p.max_growth)
    gordon_v = gordon_value(dpa_v, growth_v, p.gordon_required_return)
    gordon_u = upside(gordon_v, company.current_price)
    proj_lpa_v = projected_lpa(lpa_v, growth_v, p.projection_years)
    proj_dpa_v = projected_dpa(proj_lpa_v, company.payout_expected)
    proj_ceiling_v = projective_ceiling(proj_dpa_v, p.projective_required_yield)
    proj_u = upside(proj_ceiling_v, company.current_price)

    dy_s = score_dividend_yield(dy_v, p.bazin_min_yield)
    margin_s = score_margin(bazin_m)
    debt_s = score_debt(company.net_debt_ebitda, p.max_net_debt_ebitda, company.is_financial)
    growth_s = score_growth(company.earnings_cagr_5y)
    payout_s = score_payout(company.payout_expected, p.max_healthy_payout)
    total = excel_round(dy_s + margin_s + debt_s + growth_s + payout_s)

    return CalculationResult(
        lpa=lpa_v, dpa=dpa_v, dividend_yield=dy_v, pe_current=pe_v, pb_current=pb_v,
        graham_value=graham_v, graham_upside=graham_u, bazin_ceiling=bazin_v,
        bazin_margin=bazin_m, applied_growth=growth_v, gordon_value=gordon_v,
        gordon_upside=gordon_u, projected_lpa=proj_lpa_v, projected_dpa=proj_dpa_v,
        projective_ceiling=proj_ceiling_v, projective_upside=proj_u,
        dy_score=dy_s, margin_score=margin_s, debt_score=debt_s, growth_score=growth_s,
        payout_score=payout_s, quality_score=total, seal=seal(total)
    )
