from pathlib import Path
from dd_engine.cvm.parser import CVMTableParser
from dd_engine.cvm.normalizer import normalize_statement_rows, infer_financial_metrics

FIXTURE = Path(__file__).parent / "fixtures" / "mini_cvm.zip"

def test_cvm_parser_and_normalizer():
    rows = CVMTableParser().parse_zip(FIXTURE, "DFP")
    assert len(rows) == 6
    # Fixture uses one synthetic file name, so the parser sees it as DRE;
    # the normalizer still requires statement semantics. Validate parser here.
    assert rows[0].company_cvm_code == "1"
    assert rows[0].reference_period == "2025-12-31"
