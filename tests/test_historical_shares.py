from datetime import date
from dd_engine.cvm.shares import ShareAdjustment, adjusted_share_count, split_factor
from dd_engine.cvm.historical import HistoricalAccountingPoint, build_historical_fundamentals


def test_split_rebases_historical_shares():
    actions = [ShareAdjustment(date(2025, 6, 1), 2.0, "SPLIT")]
    assert adjusted_share_count(100, date(2024, 12, 31), actions, date(2026, 1, 1)) == 200


def test_reverse_split_factor():
    assert split_factor(1, 2) == 0.5


def test_historical_lpa_uses_adjusted_shares():
    points = [HistoricalAccountingPoint("2024", date(2024, 12, 31), 1000, 2000, 100)]
    actions = [ShareAdjustment(date(2025, 6, 1), 2.0, "SPLIT")]
    out = build_historical_fundamentals(points, actions, date(2026, 1, 1))
    assert out[0].adjusted_shares == 200
    assert out[0].lpa == 5
    assert out[0].vpa == 10


def test_invalid_action_is_ignored():
    points = [HistoricalAccountingPoint("2024", date(2024, 12, 31), 1000, None, 100)]
    actions = [ShareAdjustment(date(2025, 6, 1), 2.0, "SPLIT", status="INVALID")]
    out = build_historical_fundamentals(points, actions, date(2026, 1, 1))
    assert out[0].adjusted_shares == 100
    assert out[0].lpa == 10
