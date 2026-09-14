"""B3 market and corporate-action normalization."""

from .proventos import DividendEvent, aggregate_dpa, calculate_payout, normalize_event

__all__ = ["DividendEvent", "aggregate_dpa", "calculate_payout", "normalize_event"]
