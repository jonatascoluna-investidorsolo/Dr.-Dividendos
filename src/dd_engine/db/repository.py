from __future__ import annotations

from typing import Any

from .postgres import fetch_all, fetch_one

BASE_METRICS = """
WITH latest AS (
    SELECT DISTINCT ON (cm.company_id)
        cm.*, c.ticker, c.company_name, c.sector, c.is_financial,
        c.last_data_quality_status, c.ranking_eligible
    FROM calculated_metrics cm
    JOIN companies c ON c.id = cm.company_id
    WHERE c.is_active = true
    ORDER BY cm.company_id, cm.calculation_date DESC, cm.created_at DESC
)
"""


def list_companies(limit: int = 200, offset: int = 0) -> list[dict[str, Any]]:
    return fetch_all(
        BASE_METRICS + """
        SELECT ticker, company_name, sector, is_financial, calculation_date,
               quality_score, seal, last_data_quality_status, ranking_eligible
        FROM latest
        ORDER BY ticker
        LIMIT %s OFFSET %s
        """, (limit, offset))


def company_detail(ticker: str) -> dict[str, Any] | None:
    company = fetch_one("""
        SELECT id, ticker, company_name, sector, segment, cvm_code, cnpj,
               is_financial, is_active, last_data_quality_status,
               ranking_eligible, updated_at
        FROM companies WHERE upper(ticker)=upper(%s)
    """, (ticker,))
    if not company:
        return None
    company["latest_metrics"] = fetch_one(BASE_METRICS + """
        SELECT * FROM latest WHERE upper(ticker)=upper(%s)
    """, (ticker,)) or {}
    latest_price = fetch_one("""
        SELECT price_date, close, adjusted_close, source, validation_status, quality_score
        FROM market_prices WHERE company_id=%s
        ORDER BY price_date DESC, collected_at DESC LIMIT 1
    """, (company["id"],))
    if latest_price:
        company["latest_metrics"]["close"] = latest_price.get("close")
        company["latest_quote"] = latest_price
    company["price_history"] = fetch_all("""
        SELECT price_date, close, adjusted_close, source, currency,
               validation_status, quality_score
        FROM market_prices WHERE company_id=%s
        ORDER BY price_date DESC LIMIT 365
    """, (company["id"],))
    company["corporate_actions"] = fetch_all("""
        SELECT action_type, gross_amount_per_share, net_amount_per_share,
               adjusted_amount_per_share, declared_date, ex_date,
               record_date, payment_date, status, validation_status, source
        FROM corporate_actions WHERE company_id=%s
        ORDER BY COALESCE(ex_date, payment_date, declared_date) DESC LIMIT 200
    """, (company["id"],))
    return company


def ranking(metric: str, limit: int = 20, ascending: bool = False) -> list[dict[str, Any]]:
    allowed = {
        "graham": "graham_upside",
        "bazin": "bazin_margin",
        "gordon": "gordon_upside",
        "projective": "projective_upside",
        "quality": "quality_score",
        "dy": "dividend_yield",
    }
    column = allowed.get(metric)
    if not column:
        raise ValueError(f"Unsupported ranking metric: {metric}")
    direction = "ASC" if ascending else "DESC"
    return fetch_all(BASE_METRICS + f"""
        SELECT ticker, company_name, sector, calculation_date,
               {column} AS ranking_value, quality_score, seal,
               graham_upside, bazin_margin, gordon_upside,
               projective_upside, dividend_yield
        FROM latest
        WHERE {column} IS NOT NULL AND ranking_eligible = true
        ORDER BY {column} {direction}, ticker
        LIMIT %s
    """, (limit,))


def radar(limit: int = 50) -> list[dict[str, Any]]:
    return fetch_all(BASE_METRICS + """
        SELECT ticker, company_name, sector, calculation_date,
               quality_score, seal, dividend_yield,
               graham_upside, bazin_margin, gordon_upside,
               projective_upside, last_data_quality_status
        FROM latest
        WHERE quality_score IS NOT NULL AND ranking_eligible = true
        ORDER BY quality_score DESC, COALESCE(graham_upside, -999999) DESC
        LIMIT %s
    """, (limit,))


def quality_summary() -> dict[str, Any]:
    row = fetch_one("""
        SELECT
          count(*) FILTER (WHERE is_active) AS active_companies,
          count(*) FILTER (WHERE is_active AND last_data_quality_status='READY') AS ready_companies,
          count(*) FILTER (WHERE is_active AND last_data_quality_status='REVIEW') AS review_companies,
          count(*) FILTER (WHERE is_active AND last_data_quality_status='SOURCE_UNREACHABLE') AS unreachable_companies,
          count(*) FILTER (WHERE is_active AND ranking_eligible=true) AS ranking_eligible_companies
        FROM companies
    """) or {}
    return row
