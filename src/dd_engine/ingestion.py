from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from typing import Callable, Iterable, Optional

from .b3.proventos import DividendEvent
from .cvm.fca import TickerMapping
from .fundamentals import FundamentalInput
from .market.quotes import QuotePoint
from .pipeline import AssetSnapshot, build_asset_snapshot


@dataclass(frozen=True)
class SourceHealth:
    source: str
    checked_at: datetime
    reachable: bool
    detail: str = ""


@dataclass(frozen=True)
class AssetIngestionResult:
    ticker: str
    snapshot: Optional[AssetSnapshot]
    errors: tuple[str, ...] = ()


@dataclass
class EODIngestionRun:
    as_of: date
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    results: list[AssetIngestionResult] = field(default_factory=list)
    source_health: list[SourceHealth] = field(default_factory=list)

    @property
    def finished_at(self) -> datetime:
        return datetime.now(timezone.utc)

    @property
    def ready_count(self) -> int:
        return sum(r.snapshot is not None and r.snapshot.status == "READY" for r in self.results)

    @property
    def review_count(self) -> int:
        return sum(r.snapshot is not None and r.snapshot.status == "REVIEW" for r in self.results)


def run_eod_ingestion(
    tickers: Iterable[str],
    as_of: date,
    quote_loader: Callable[[str, date], Iterable[QuotePoint]],
    provento_loader: Callable[[str, date], Iterable[DividendEvent]],
    fundamental_loader: Callable[[str, date], FundamentalInput | None],
) -> EODIngestionRun:
    """Execute the production-shaped EOD boundary with per-asset fault isolation."""
    run = EODIngestionRun(as_of=as_of)
    for raw_ticker in tickers:
        ticker = raw_ticker.upper().strip()
        errors: list[str] = []
        try:
            snapshot = build_asset_snapshot(
                ticker,
                as_of,
                quote_loader(ticker, as_of),
                provento_loader(ticker, as_of),
                fundamental_loader(ticker, as_of),
            )
        except Exception as exc:  # one bad issuer must not stop the 93-asset run
            snapshot = None
            errors.append(f"{type(exc).__name__}: {exc}")
        run.results.append(AssetIngestionResult(ticker=ticker, snapshot=snapshot, errors=tuple(errors)))
    return run


def validate_ticker_mapping(
    expected_tickers: Iterable[str],
    mappings: Iterable[TickerMapping],
) -> tuple[list[str], list[str]]:
    """Return (matched, missing) without inventing mappings."""
    expected = {t.upper().strip() for t in expected_tickers}
    found = {m.ticker.upper().strip() for m in mappings if m.ticker}
    return sorted(expected & found), sorted(expected - found)
