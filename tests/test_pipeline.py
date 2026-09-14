from datetime import date

from dd_engine.pipeline import build_asset_snapshot, run_universe_pipeline
from dd_engine.market.quotes import QuotePoint
from dd_engine.b3.proventos import DividendEvent


def test_asset_snapshot_ready_with_quote_and_events():
    d = date(2026, 9, 10)
    q = QuotePoint("PETR4", d, 35.0, "B3")
    e = DividendEvent("PETR4", "DIVIDEND", 0.5, ex_date=date(2026, 8, 10), source_event_id="x")
    s = build_asset_snapshot("petr4", d, [q], [e], None)
    assert s.ticker == "PETR4"
    assert s.quote.close == 35.0
    assert s.dpa_ltm == 0.5
    assert s.status == "REVIEW"


def test_pipeline_runs_for_universe():
    d = date(2026, 9, 10)
    def quotes(t, _): return [QuotePoint(t, d, 10.0, "YAHOO")]
    def events(t, _): return []
    def fundamentals(t, _): return None
    result = run_universe_pipeline(["PETR4", "ABEV3"], d, quotes, events, fundamentals)
    assert [x.ticker for x in result] == ["PETR4", "ABEV3"]
    assert all(x.status == "REVIEW" for x in result)
