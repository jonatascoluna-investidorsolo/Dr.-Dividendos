from datetime import date

from dd_engine.b3.proventos import (
    DividendEvent, adjusted_provento, aggregate_dpa, calculate_payout,
    deduplicate_events, normalize_event,
)


def ev(**kw):
    base = dict(ticker="PETR4", action_type="DIVIDEND", gross_amount_per_share=1.0,
                ex_date=date(2026, 6, 1), source_event_id="evt-1")
    base.update(kw)
    return DividendEvent(**base)


def test_normalize_and_aliases():
    x = normalize_event(ev(action_type="dividendos", ticker="petr4"))
    assert x.action_type == "DIVIDEND"
    assert x.ticker == "PETR4"
    assert x.event_fingerprint


def test_dedup_source_event_id():
    a = ev(gross_amount_per_share=1.0)
    b = ev(gross_amount_per_share=1.2)
    assert len(deduplicate_events([a, b])) == 1


def test_dedup_without_source_id_uses_fingerprint():
    a = ev(source_event_id=None)
    b = ev(source_event_id=None)
    assert len(deduplicate_events([a, b])) == 1


def test_cancelled_event_is_excluded():
    a = ev(gross_amount_per_share=1.0)
    b = ev(gross_amount_per_share=9.0, source_event_id="cancelled", status="CANCELLED")
    assert aggregate_dpa([a, b], date(2026, 1, 1), date(2026, 12, 31)) == 1.0


def test_split_adjusts_historical_dpa_to_current_basis():
    a = ev(gross_amount_per_share=1.0, source_event_id="old")
    adjusted = adjusted_provento(a, [2.0])
    assert adjusted.adjusted_amount == 0.5


def test_aggregate_dividend_and_jcp():
    events = [
        ev(gross_amount_per_share=0.4, source_event_id="d1"),
        ev(action_type="JCP", gross_amount_per_share=0.2, source_event_id="j1", ex_date=date(2026, 7, 1)),
    ]
    assert aggregate_dpa(events, date(2026, 1, 1), date(2026, 12, 31)) == 0.6


def test_payout_uses_gross_jcp_and_returns_none_for_loss():
    assert calculate_payout(1.0, 100.0, 100.0) == 1.0
    assert calculate_payout(1.0, 0.0, 100.0) is None
    assert calculate_payout(1.0, -10.0, 100.0) is None
