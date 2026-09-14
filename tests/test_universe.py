from pathlib import Path
from dd_engine.cvm.universe import load_excel_universe

def test_universe_has_93_assets():
    path=Path('/mnt/data/Planilha_Doutor_dos_Dividendos_v2.xlsx')
    items=load_excel_universe(path)
    assert len(items)==93
    assert any(x.ticker=='PETR4' for x in items)
    assert any(x.ticker=='STOC34' and x.likely_bdr for x in items)
