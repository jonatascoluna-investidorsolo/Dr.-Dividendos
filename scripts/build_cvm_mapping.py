from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"src"))
import csv
from dd_engine.cvm.universe import load_excel_universe, write_manifest

ROOT=Path(__file__).resolve().parents[1]
EXCEL=ROOT.parent/'Planilha_Doutor_dos_Dividendos_v2.xlsx'
OUT=ROOT/'data/reference/doutor_dos_dividendos_universe.csv'

items=load_excel_universe(EXCEL)
write_manifest(items, OUT)
print(f'Universo exportado: {len(items)} ativos -> {OUT}')
print(f'BDRs prováveis por heurística de ticker: {sum(x.likely_bdr for x in items)}')
