from datetime import date

from dd_engine.pipeline import AssetSnapshot
from dd_engine.repository import build_persistence_plan, postgres_upsert_sql
from dd_engine.cvm.canonical import AccountingSnapshot


def test_persistence_plan_keeps_missing_data_as_none():
    s = AssetSnapshot("PETR4", date(2026, 9, 10), None, None, None, "REVIEW", ("QUOTE_MISSING",))
    p = build_persistence_plan(s, "company-1")
    assert p.price is None
    assert p.metrics is None
    assert p.quality_events[0]["field_name"] == "QUOTE_MISSING"


def test_persistence_plan_contains_quote_and_metrics():
    from dd_engine.market.quotes import QuotePoint
    from dd_engine.fundamentals import FundamentalInput, calculate_fundamentals
    q = QuotePoint("PETR4", date(2026, 9, 10), 35.0, "YAHOO")
    f = calculate_fundamentals(FundamentalInput(
        snapshot=AccountingSnapshot(
            company_cvm_code="123", company_name="Petroleo", document_type="ITR",
            reference_period="2026-06-30", disclosure_date="2026-08-01", version=1,
            net_income=1000, attributable_net_income=1000,
            equity_attributable_common=2000, cash_and_equivalents=100,
            financial_debt=500, net_debt=400, ebitda=266.6667, debt_ebitda=1.5,
            quality_flags=(), evidence={}
        ),
        shares=100, price=35, payout=.5, historical=()
    ))
    s = AssetSnapshot("PETR4", date(2026, 9, 10), q, 1.2, f, "READY")
    p = build_persistence_plan(s, "company-1")
    assert p.price["close"] == 35.0
    assert p.metrics["dpa"] == 1.2


def test_upsert_sql_is_idempotent():
    sql = postgres_upsert_sql()
    assert "ON CONFLICT (company_id, price_date, source)" in sql
    assert "DO UPDATE SET" in sql
