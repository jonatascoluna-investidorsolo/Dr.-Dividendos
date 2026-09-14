from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from dd_engine.cvm.client import CVMClient
from dd_engine.cvm.fca import parse_fca_zip
from dd_engine.cvm.universe import load_excel_universe

parser=argparse.ArgumentParser(description='Relaciona os tickers do Doutor dos Dividendos com a FCA/CVM.')
parser.add_argument('--excel', default='../Planilha_Doutor_dos_Dividendos_v2.xlsx')
parser.add_argument('--year', type=int, default=2026)
parser.add_argument('--workdir', default='data/cvm')
args=parser.parse_args()

root=Path(__file__).resolve().parents[1]
excel=(root/args.excel).resolve() if not Path(args.excel).is_absolute() else Path(args.excel)
work=root/args.workdir; work.mkdir(parents=True, exist_ok=True)
fca=work/f'fca_cia_aberta_{args.year}.zip'
client=CVMClient()
if not fca.exists():
    print(f'Baixando FCA {args.year} da CVM...')
    client.download_fca(args.year, fca)
rows=parse_fca_zip(fca)
by={}
for r in rows:
    by.setdefault(r.ticker, []).append(r)
items=load_excel_universe(excel)
matched=[]; missing=[]
for item in items:
    candidates=by.get(item.ticker, [])
    if candidates:
        matched.append((item,candidates))
    else:
        missing.append(item)
print(f'Universo Excel: {len(items)}')
print(f'Match FCA/CVM: {len(matched)}')
print(f'Sem match: {len(missing)}')
if missing:
    print('Tickers sem match:')
    for x in missing: print(f'  {x.ticker} | {x.company_name}')
