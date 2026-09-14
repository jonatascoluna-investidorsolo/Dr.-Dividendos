from dd_engine.cvm.parser import StatementRow
from dd_engine.cvm.normalizer import normalize_statement_rows, infer_financial_metrics

def r(stmt, code, name, value):
    return StatementRow("DFP", "1", "Teste SA", "2025-12-31", "2026-03-01", 1, stmt, code, name, value, "ÚLTIMO", {})

def test_canonical_mapping_and_debt_no_double_count():
    rows = [
        r("DRE", "1", "Lucro líquido do período", 100),
        r("BPP", "2", "Patrimônio líquido atribuível aos acionistas da companhia controladora", 500),
        r("BPA", "3", "Caixa e equivalentes de caixa", 80),
        r("BPP", "4", "Empréstimos e financiamentos - circulante", 100),
        r("BPP", "5", "Empréstimos e financiamentos - não circulante", 80),
        r("DRE", "6", "EBITDA", 200),
        r("BPP", "7", "Empréstimos e financiamentos", 180), # parent/total: must not be added
    ]
    m = normalize_statement_rows(rows)[0]
    assert m.net_income == 100
    assert m.equity_attributable_common == 500
    assert m.cash_and_equivalents == 80
    assert m.financial_debt == 180
    assert infer_financial_metrics(m)["debt_ebitda"] == 0.5
    assert "attributable_net_income_not_found_using_net_income" in m.quality_flags

def test_attributable_net_income_has_priority():
    rows = [
        r("DRE", "1", "Lucro líquido do período", 100),
        r("DRE", "2", "Lucro atribuível aos acionistas da companhia controladora", 90),
    ]
    m = normalize_statement_rows(rows)[0]
    assert m.net_income == 100
    assert m.attributable_net_income == 90
