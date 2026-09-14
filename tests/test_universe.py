from pathlib import Path

from dd_engine.cvm.universe import UniverseItem


def test_universe_has_93_assets():
    path = Path("data/reference/doutor_dos_dividendos_universe.csv")

    rows = path.read_text(encoding="utf-8").splitlines()

    # Cabeçalho + 93 ativos
    assert len(rows) == 94

    assert any("PETR4" in row for row in rows)
    assert any("STOC34" in row and "True" in row for row in rows)
