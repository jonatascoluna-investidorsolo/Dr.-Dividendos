from dd_engine.cvm.parser import StatementRow
from dd_engine.cvm.canonical import build_accounting_snapshots, select_latest_snapshot


def r(version, period, value=100):
    return StatementRow("DFP", "1", "Teste SA", period, f"{period[:4]}-03-01", version, "DRE", "1", "Lucro líquido do período", value, "ÚLTIMO", {})


def test_restatement_version_wins_for_same_period():
    snaps = build_accounting_snapshots([r(1, "2025-12-31", 100), r(2, "2025-12-31", 120)])
    latest = select_latest_snapshot(snaps)
    assert latest.version == 2
    assert latest.net_income == 120


def test_snapshot_contains_net_debt_and_evidence():
    rows = [
        r(1, "2025-12-31", 100),
        StatementRow("DFP", "1", "Teste SA", "2025-12-31", "2026-03-01", 1, "BPA", "2", "Caixa e equivalentes de caixa", 20, "ÚLTIMO", {}),
        StatementRow("DFP", "1", "Teste SA", "2025-12-31", "2026-03-01", 1, "BPP", "3", "Empréstimos e financiamentos - circulante", 50, "ÚLTIMO", {}),
        StatementRow("DFP", "1", "Teste SA", "2025-12-31", "2026-03-01", 1, "BPP", "4", "Empréstimos e financiamentos - não circulante", 30, "ÚLTIMO", {}),
    ]
    snap = build_accounting_snapshots(rows)[0]
    assert snap.financial_debt == 80
    assert snap.net_debt == 60
    assert "net_income" in snap.evidence
