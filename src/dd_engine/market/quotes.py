from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date, datetime, timezone
from typing import Iterable, Optional


@dataclass(frozen=True)
class QuotePoint:
    ticker: str
    price_date: date
    close: float
    source: str
    currency: str = "BRL"
    collected_at: Optional[datetime] = None
    is_adjusted: bool = False
    validation_status: str = "VALID"
    quality_score: int = 100
    source_symbol: Optional[str] = None

    def __post_init__(self) -> None:
        if self.close < 0:
            raise ValueError("close must be non-negative")


def normalize_quote(q: QuotePoint) -> QuotePoint:
    ticker = q.ticker.upper().strip()
    source = q.source.upper().strip()
    collected = q.collected_at or datetime.now(timezone.utc)
    return replace(q, ticker=ticker, source=source, collected_at=collected)


def validate_quote(q: QuotePoint, expected_currency: str = "BRL") -> QuotePoint:
    q = normalize_quote(q)
    score = 100
    status = "VALID"
    if q.close <= 0:
        status = "INVALID"
        score -= 80
    if q.currency.upper() != expected_currency.upper():
        status = "REVIEW"
        score -= 30
    if q.price_date > q.collected_at.date():
        status = "INVALID"
        score -= 50
    return replace(q, validation_status=status, quality_score=max(0, score))


def select_preferred_quote(quotes: Iterable[QuotePoint], target_date: date) -> Optional[QuotePoint]:
    """Select the highest-quality quote for a target trading date.

    Preference: valid > review, then official/B3-like source, then source priority,
    then latest collection. Never silently use a different trading date.
    """
    candidates = [validate_quote(q) for q in quotes if q.price_date == target_date]
    candidates = [q for q in candidates if q.validation_status in {"VALID", "REVIEW"}]
    if not candidates:
        return None
    priority = {"B3": 3, "UP2DATA": 3, "YAHOO": 2, "GOOGLE": 1}
    return max(candidates, key=lambda q: (q.validation_status == "VALID", priority.get(q.source, 0), q.quality_score, q.collected_at or datetime.min.replace(tzinfo=timezone.utc)))
