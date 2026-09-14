from dd_engine.cvm.itub4 import filter_cvm_code
from dd_engine.cvm.parser import StatementRow


def row(code):
    return StatementRow("DFP", code, "Banco", "2025-12-31", "2026-02-01", 1, "DRE", "1", "Lucro", 10, "ÚLTIMO", {})


def test_filter_cvm_code_is_strict():
    rows = [row("19348"), row("19349"), row(None)]
    out = filter_cvm_code(rows, "19348")
    assert len(out) == 1
    assert out[0].company_cvm_code == "19348"
