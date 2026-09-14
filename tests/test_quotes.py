from datetime import date, datetime, timezone

from dd_engine.market.quotes import QuotePoint, normalize_quote, validate_quote, select_preferred_quote


def q(**kw):
    base = dict(ticker="PETR4", price_date=date(2026, 9, 10), close=35.5,
                source="yahoo", collected_at=datetime(2026, 9, 11, tzinfo=timezone.utc))
    base.update(kw)
    return QuotePoint(**base)


def test_normalize_quote():
    x = normalize_quote(q(ticker=" petr4 "))
    assert x.ticker == "PETR4"
    assert x.source == "YAHOO"


def test_invalid_nonpositive_quote():
    assert validate_quote(q(close=0)).validation_status == "INVALID"


def test_future_quote_date_invalid():
    x = validate_quote(q(price_date=date(2026, 9, 12)))
    assert x.validation_status == "INVALID"


def test_prefer_b3_over_yahoo_same_day():
    yahoo = q(source="YAHOO", close=35.5)
    b3 = q(source="B3", close=35.6)
    chosen = select_preferred_quote([yahoo, b3], date(2026, 9, 10))
    assert chosen.source == "B3"
    assert chosen.close == 35.6


def test_never_substitute_another_date():
    assert select_preferred_quote([q(price_date=date(2026, 9, 9))], date(2026, 9, 10)) is None
