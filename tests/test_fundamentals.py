from dd_engine.cvm.parser import StatementRow
from dd_engine.cvm.canonical import build_accounting_snapshots
from dd_engine.fundamentals import FundamentalInput, HistoricalPoint, calculate_fundamentals, earnings_cagr_5y


def r(stmt, code, name, value):
    return StatementRow('DFP','1','Teste SA','2025-12-31','2026-03-01',1,stmt,code,name,value,'ÚLTIMO',{})


def snap():
    return build_accounting_snapshots([
        r('DRE','1','Lucro líquido do período',100),
        r('DRE','2','Lucro atribuível aos acionistas da companhia controladora',90),
        r('BPP','3','Patrimônio líquido atribuível aos acionistas da companhia controladora',500),
        r('BPA','4','Caixa e equivalentes de caixa',80),
        r('BPP','5','Empréstimos e financiamentos - circulante',100),
        r('BPP','6','Empréstimos e financiamentos - não circulante',80),
        r('DRE','7','EBITDA',200),
    ])[0]


def test_earnings_cagr_requires_five_year_interval():
    pts=[HistoricalPoint('2020-12-31',50),HistoricalPoint('2025-12-31',90)]
    assert abs(earnings_cagr_5y(pts) - ((90/50)**(1/5)-1)) < 1e-12
    assert earnings_cagr_5y([HistoricalPoint('2022-12-31',50),HistoricalPoint('2025-12-31',90)]) is None


def test_fundamentals_calculate_core_metrics():
    m=calculate_fundamentals(FundamentalInput(
        snapshot=snap(), shares=10, price=8, payout=.5,
        historical=[HistoricalPoint('2020-12-31',50),HistoricalPoint('2025-12-31',90)]
    ))
    assert m.lpa == 9
    assert m.vpa == 50
    assert m.dpa == 4.5
    assert m.pe_current == 8/9
    assert m.pb_current == .16
    assert m.cagr_5y is not None


def test_financial_institution_excludes_debt_ebitda_from_score():
    m=calculate_fundamentals(FundamentalInput(snapshot=snap(), shares=10, price=8, payout=.5, financial_institution=True))
    assert m.debt_score == 0
    assert 'financial_institution_debt_ebitda_not_applicable' in m.flags
