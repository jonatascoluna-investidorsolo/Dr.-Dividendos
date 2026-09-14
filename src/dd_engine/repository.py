from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any, Iterable


@dataclass(frozen=True)
class PersistencePlan:
    """Database-agnostic write plan; execution is intentionally separate."""
    company: dict[str, Any]
    price: dict[str, Any] | None
    corporate_actions: tuple[dict[str, Any], ...]
    financial_statements: tuple[dict[str, Any], ...]
    metrics: dict[str, Any] | None
    quality_events: tuple[dict[str, Any], ...]


def _clean(value: Any) -> Any:
    if isinstance(value, Decimal):
        return float(value)
    return value


def build_persistence_plan(snapshot: Any, company_id: str, calculation_version: str = "v1.4") -> PersistencePlan:
    """Turn a computed snapshot into idempotent-ready records without writing them.

    The database layer can upsert these records. Historical records are never
    deleted by this plan; the calculation date/version forms the immutable key.
    """
    company = {
        "id": company_id,
        "ticker": snapshot.ticker,
        "updated_at": snapshot.as_of,
    }
    price = None
    if snapshot.quote is not None:
        q = snapshot.quote
        price = {
            "company_id": company_id,
            "price_date": q.price_date,
            "close": _clean(q.close),
            "source": q.source,
            "source_symbol": getattr(q, "source_symbol", None),
            "currency": getattr(q, "currency", "BRL"),
            "validation_status": getattr(q, "validation_status", "VALID"),
            "quality_score": getattr(q, "quality_score", 100),
        }

    metrics = None
    if snapshot.fundamental is not None:
        f = snapshot.fundamental
        metrics = {
            "company_id": company_id,
            "calculation_date": snapshot.as_of,
            "lpa": getattr(f, "lpa", None),
            "vpa": getattr(f, "vpa", None),
            "dpa": snapshot.dpa_ltm,
            "dividend_yield": getattr(f, "dividend_yield", None),
            "pe_current": getattr(f, "pe_current", None),
            "pb_current": getattr(f, "pb_current", None),
            "graham_value": getattr(f, "graham_value", None),
            "graham_upside": getattr(f, "graham_upside", None),
            "bazin_ceiling": getattr(f, "bazin_ceiling", None),
            "bazin_margin": getattr(f, "bazin_margin", None),
            "applied_growth": getattr(f, "applied_growth", None),
            "gordon_value": getattr(f, "gordon_value", None),
            "gordon_upside": getattr(f, "gordon_upside", None),
            "projected_lpa": getattr(f, "projected_lpa", None),
            "projected_dpa": getattr(f, "projected_dpa", None),
            "projective_ceiling": getattr(f, "projective_ceiling", None),
            "projective_upside": getattr(f, "projective_upside", None),
            "calculation_version": calculation_version,
        }

    quality = tuple({
        "company_id": company_id,
        "field_name": flag,
        "reason": flag,
        "status": "PENDING",
    } for flag in snapshot.quality_flags)
    return PersistencePlan(company, price, (), (), metrics, quality)


def postgres_upsert_sql() -> str:
    """Canonical SQL template used by the production repository adapter."""
    return """
INSERT INTO market_prices
(company_id, price_date, close, source, source_symbol, currency, validation_status, quality_score)
VALUES (%(company_id)s, %(price_date)s, %(close)s, %(source)s, %(source_symbol)s,
        %(currency)s, %(validation_status)s, %(quality_score)s)
ON CONFLICT (company_id, price_date, source)
DO UPDATE SET close=EXCLUDED.close,
              source_symbol=EXCLUDED.source_symbol,
              currency=EXCLUDED.currency,
              validation_status=EXCLUDED.validation_status,
              quality_score=EXCLUDED.quality_score;
""".strip()
