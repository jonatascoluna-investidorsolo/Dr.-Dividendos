from dd_engine.cvm.fca import TickerMapping
from dd_engine.cvm.universe import UniverseItem
from dd_engine.validation import validate_universe


def test_universe_validation_match_missing_and_bdr():
    items = [
        UniverseItem(8, "Petrobras", "PETR4", False, "Energia"),
        UniverseItem(9, "Stone", "STOC34", True, "Financeiro"),
        UniverseItem(10, "X", "XXXX3", False, "Outro"),
    ]
    mappings = [TickerMapping("PETR4", "9512", "Petróleo Brasileiro S.A.", "00000000000191", "fca.csv", {})]
    rows = validate_universe(items, mappings)
    assert [r.status for r in rows] == ["MATCH", "SPECIAL_HANDLING", "MISSING"]
    assert rows[0].cvm_code == "9512"
