from dd_engine.cvm.parser import StatementRow
from dd_engine.cvm.canonical import build_accounting_snapshots
from dd_engine.cvm.periods import latest_by_reference_period, select_latest_annual, build_historical_annual_series


def row(version, period, value, doc="DFP"):
    return StatementRow(doc, "1", "Teste SA", period, f"{period[:4]}-03-01", version,
                        "DRE", "1", "Lucro líquido do período", value, "ÚLTIMO", {})


def test_latest_by_reference_period_resolves_restatement_but_keeps_history():
    snaps = build_accounting_snapshots([
        row(1, "2024-12-31", 80), row(1, "2025-12-31", 100),
        row(1, "2025-12-31", 120), row(2, "2025-12-31", 130),
    ])
    result = latest_by_reference_period(snaps)
    assert len(result) == 2
    assert [x.reference_period for x in result] == ["2024-12-31", "2025-12-31"]
    assert result[-1].version == 2
    assert result[-1].net_income == 130


def test_select_latest_annual_ignores_itr():
    snaps = build_accounting_snapshots([
        row(1, "2025-12-31", 100, "DFP"),
        row(1, "2026-06-30", 140, "ITR"),
    ])
    latest = select_latest_annual(snaps)
    assert latest.document_type == "DFP"
    assert latest.reference_period == "2025-12-31"


def test_historical_annual_series_is_one_per_period():
    snaps = build_accounting_snapshots([
        row(1, "2023-12-31", 70), row(1, "2024-12-31", 80),
        row(1, "2024-12-31", 90), row(1, "2025-12-31", 100),
    ])
    series = build_historical_annual_series(snaps)
    assert len(series) == 3
    assert [s.net_income for s in series] == [70, 80, 100]
