import json
from dataclasses import asdict

from dd_engine.models import CompanyInput
from dd_engine.service import calculate_company

sample = CompanyInput(
    ticker="EXEMPLO3",
    company_name="Empresa Exemplo",
    shares=100_000_000,
    projected_net_income=200_000_000,
    book_value_per_share=12.0,
    net_debt_ebitda=1.2,
    earnings_cagr_5y=0.10,
    payout_expected=0.60,
    current_price=18.0,
)

print(json.dumps(asdict(calculate_company(sample)), indent=2, ensure_ascii=False))
