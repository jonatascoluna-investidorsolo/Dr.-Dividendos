from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date
from decimal import Decimal
from hashlib import sha256
from typing import Iterable, Optional


CASH_ACTIONS = {"DIVIDEND", "JCP", "CASH_BONUS", "YIELD"}
VALID_STATUSES = {"VALID", "CONFIRMED", "ACTIVE"}
INVALID_STATUSES = {"CANCELLED", "CANCELED", "REJECTED", "VOID"}


@dataclass(frozen=True)
class DividendEvent:
    ticker: str
    action_type: str
    gross_amount_per_share: float
    announcement_date: Optional[date] = None
    ex_date: Optional[date] = None
    record_date: Optional[date] = None
    payment_date: Optional[date] = None
    source: str = "B3"
    source_event_id: Optional[str] = None
    status: str = "VALID"
    currency: str = "BRL"
    adjustment_factor: float = 1.0
    adjusted_amount_per_share: Optional[float] = None
    validation_status: str = "VALID"
    event_fingerprint: Optional[str] = None

    def __post_init__(self) -> None:
        if self.gross_amount_per_share < 0:
            raise ValueError("gross_amount_per_share must be non-negative")
        if self.adjustment_factor <= 0:
            raise ValueError("adjustment_factor must be positive")
        if _norm_action(self.action_type) not in CASH_ACTIONS:
            raise ValueError(f"Unsupported cash action: {self.action_type}")

    @property
    def adjusted_amount(self) -> float:
        if self.adjusted_amount_per_share is not None:
            return self.adjusted_amount_per_share
        return self.gross_amount_per_share * self.adjustment_factor


def _norm_action(value: str) -> str:
    raw = value.strip().upper().replace("-", "_").replace(" ", "_")
    aliases = {"DIVIDENDOS": "DIVIDEND", "DIVIDENDO": "DIVIDEND", "JUROS_SOBRE_CAPITAL_PROPRIO": "JCP", "JUROS_SOBRE_CAPITAL": "JCP"}
    return aliases.get(raw, raw)


def _fingerprint(event: DividendEvent) -> str:
    parts = [
        event.ticker.upper().strip(), _norm_action(event.action_type),
        f"{Decimal(str(event.gross_amount_per_share)):.12f}",
        event.announcement_date.isoformat() if event.announcement_date else "",
        event.ex_date.isoformat() if event.ex_date else "",
        event.record_date.isoformat() if event.record_date else "",
        event.payment_date.isoformat() if event.payment_date else "",
    ]
    return sha256("|".join(parts).encode()).hexdigest()


def normalize_event(event: DividendEvent) -> DividendEvent:
    status = event.status.upper().strip()
    validation = "INVALID" if status in INVALID_STATUSES else event.validation_status.upper()
    normalized = replace(
        event,
        ticker=event.ticker.upper().strip(),
        action_type=_norm_action(event.action_type),
        status=status,
        validation_status=validation,
    )
    return replace(normalized, event_fingerprint=normalized.event_fingerprint or _fingerprint(normalized))


def deduplicate_events(events: Iterable[DividendEvent]) -> list[DividendEvent]:
    """Keep one canonical event; source_event_id wins over a deterministic fingerprint."""
    result: dict[str, DividendEvent] = {}
    for raw in events:
        event = normalize_event(raw)
        if event.status in INVALID_STATUSES or event.validation_status == "INVALID":
            continue
        key = f"id:{event.source_event_id}" if event.source_event_id else f"fp:{event.event_fingerprint}"
        result[key] = event
    return list(result.values())


def adjusted_provento(event: DividendEvent, future_adjustment_factors: Iterable[float]) -> DividendEvent:
    """Restate a historical per-share cash distribution to a later share basis.

    Example: after a 2-for-1 split, a historical R$1.00/share dividend becomes
    R$0.50/share on the current share basis, hence the factor 1/2.
    """
    factor = event.adjustment_factor
    for f in future_adjustment_factors:
        if f <= 0:
            raise ValueError("share adjustment factors must be positive")
        factor *= 1.0 / f
    return replace(event, adjustment_factor=factor, adjusted_amount_per_share=event.gross_amount_per_share * factor)


def aggregate_dpa(events: Iterable[DividendEvent], start: date, end: date) -> float:
    """Aggregate realized cash distributions using ex-date as entitlement date."""
    total = 0.0
    for event in deduplicate_events(events):
        if event.ex_date is None or not (start <= event.ex_date <= end):
            continue
        total += event.adjusted_amount
    return round(total, 12)


def calculate_payout(dpa_realized: Optional[float], attributable_net_income: Optional[float], shares: Optional[float]) -> Optional[float]:
    """Payout = total distributions / attributable earnings.

    For company-level analysis, JCP is kept at gross declared amount. Payout is
    not manufactured when earnings are zero/negative or the share base is invalid.
    """
    if dpa_realized is None or attributable_net_income is None or shares is None:
        return None
    if attributable_net_income <= 0 or shares <= 0:
        return None
    distributions = dpa_realized * shares
    return distributions / attributable_net_income
