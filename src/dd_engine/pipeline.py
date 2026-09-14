from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Callable, Iterable, Optional

from .b3.proventos import DividendEvent, aggregate_dpa
from .fundamentals import FundamentalInput, calculate_fundamentals
from .market.quotes import QuotePoint, select_preferred_quote


@dataclass(frozen=True)
class AssetSnapshot:
    ticker: str
    as_of: date
    quote: Optional[QuotePoint]
    dpa_ltm: Optional[float]
    fundamental: object | None
    status: str
    quality_flags: tuple[str, ...] = ()


def build_asset_snapshot(
    ticker: str,
    as_of: date,
    quotes: Iterable[QuotePoint],
    proventos: Iterable[DividendEvent],
    fundamental_input: FundamentalInput | None = None,
) -> AssetSnapshot:
    flags: list[str] = []
    quote = select_preferred_quote(quotes, as_of)
    if quote is None:
        flags.append("QUOTE_MISSING")
    events = list(proventos)
    # LTM uses entitlement/ex-date. This is intentionally separate from fiscal-year payout.
    start = date(as_of.year - 1, as_of.month, as_of.day)
    dpa_ltm = aggregate_dpa(events, start, as_of) if events else None
    if not events:
        flags.append("PROVENTOS_MISSING")
    fundamentals = calculate_fundamentals(fundamental_input) if fundamental_input else None
    if fundamental_input is None:
        flags.append("FUNDAMENTALS_MISSING")
    status = "READY" if not flags else "REVIEW"
    return AssetSnapshot(
        ticker=ticker.upper().strip(),
        as_of=as_of,
        quote=quote,
        dpa_ltm=dpa_ltm,
        fundamental=fundamentals,
        status=status,
        quality_flags=tuple(flags),
    )


def run_universe_pipeline(
    tickers: Iterable[str],
    as_of: date,
    quote_loader: Callable[[str, date], Iterable[QuotePoint]],
    provento_loader: Callable[[str, date], Iterable[DividendEvent]],
    fundamental_loader: Callable[[str, date], FundamentalInput | None],
) -> list[AssetSnapshot]:
    """Run one deterministic EOD cycle for the configured universe.

    The loader boundaries make the production job replaceable: B3/CVM/Yahoo
    adapters can be used without changing the calculation engine.
    """
    out: list[AssetSnapshot] = []
    for ticker in tickers:
        t = ticker.upper().strip()
        out.append(build_asset_snapshot(
            t,
            as_of,
            quote_loader(t, as_of),
            provento_loader(t, as_of),
            fundamental_loader(t, as_of),
        ))
    return out
