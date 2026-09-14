from __future__ import annotations

import json
import urllib.parse
import urllib.request
from abc import ABC, abstractmethod
from datetime import date, datetime, timezone
from typing import Any, Iterable

from .quotes import QuotePoint


class QuoteProvider(ABC):
    name: str

    @abstractmethod
    def fetch_daily_close(self, ticker: str, start: date, end: date) -> list[QuotePoint]:
        raise NotImplementedError


class YahooChartProvider(QuoteProvider):
    """Yahoo Finance chart endpoint adapter.

    The provider is intentionally isolated from the calculation engine. In
    production, keep B3/UP2DATA as the preferred source when licensed/available
    and use Yahoo as validation/fallback.
    """

    name = "YAHOO"
    base_url = "https://query1.finance.yahoo.com/v8/finance/chart/"

    def __init__(self, timeout: int = 20, user_agent: str = "DoutorDosDividendos/1.1") -> None:
        self.timeout = timeout
        self.user_agent = user_agent

    @staticmethod
    def _epoch(d: date) -> int:
        return int(datetime(d.year, d.month, d.day, tzinfo=timezone.utc).timestamp())

    @staticmethod
    def _symbol(ticker: str) -> str:
        t = ticker.upper().strip()
        # Yahoo commonly uses .SA for B3-listed Brazilian equities.
        return t if t.endswith(".SA") else f"{t}.SA"

    def fetch_daily_close(self, ticker: str, start: date, end: date) -> list[QuotePoint]:
        symbol = self._symbol(ticker)
        params = urllib.parse.urlencode({
            "period1": self._epoch(start),
            "period2": self._epoch(end),
            "interval": "1d",
            "events": "history",
            "includeAdjustedClose": "true",
        })
        url = f"{self.base_url}{urllib.parse.quote(symbol)}?{params}"
        request = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            payload: dict[str, Any] = json.load(response)
        result = payload.get("chart", {}).get("result") or []
        if not result:
            return []
        row = result[0]
        timestamps = row.get("timestamp") or []
        quote = ((row.get("indicators") or {}).get("quote") or [{}])[0]
        closes = quote.get("close") or []
        out: list[QuotePoint] = []
        for ts, close in zip(timestamps, closes):
            if close is None:
                continue
            dt = datetime.fromtimestamp(ts, tz=timezone.utc)
            out.append(QuotePoint(
                ticker=ticker,
                price_date=dt.date(),
                close=float(close),
                source=self.name,
                currency="BRL",
                collected_at=datetime.now(timezone.utc),
                source_symbol=symbol,
            ))
        return out
