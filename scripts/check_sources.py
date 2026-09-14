from __future__ import annotations
import json
from pathlib import Path
from dd_engine.source_health import Endpoint, check_sources

ROOT = Path(__file__).resolve().parents[1]
endpoints = [
    Endpoint("CVM_DFP", "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/dfp_cia_aberta_2026.zip"),
    Endpoint("CVM_ITR", "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/itr_cia_aberta_2026.zip"),
    Endpoint("CVM_CADASTRO", "https://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv"),
    Endpoint("CVM_FCA", "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/FCA/DADOS/fca_cia_aberta_2026.zip"),
    Endpoint("B3_UP2DATA", "https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/up2data/dados-disponiveis/"),
    Endpoint("YAHOO", "https://query1.finance.yahoo.com/v8/finance/chart/PETR4.SA"),
]
result = check_sources(endpoints)
print(json.dumps(result, indent=2, ensure_ascii=False))
