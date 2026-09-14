from dd_engine.models import CompanyInput
from dd_engine.service import calculate_company


def test_full_company_calculation():
    c = CompanyInput(
        ticker="TEST3", company_name="Empresa Teste", shares=100,
        projected_net_income=200, book_value_per_share=10,
        net_debt_ebitda=1, earnings_cagr_5y=0.10,
        payout_expected=0.60, current_price=20,
    )
    r = calculate_company(c)
    assert r.lpa == 2
    assert r.dpa == 1.2
    assert r.graham_value is not None
    assert r.bazin_ceiling == 20
    assert r.applied_growth == 0.06
    assert r.quality_score >= 0
