from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import csv, io, zipfile
from typing import Iterable

@dataclass(frozen=True)
class TickerMapping:
    ticker: str
    cvm_code: str | None
    company_name: str | None
    cnpj: str | None
    source_file: str
    raw: dict[str, str]

def _read_csv(raw: bytes) -> Iterable[dict[str,str]]:
    text = raw.decode('latin-1')
    sample = text[:8192]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=';,	')
    except csv.Error:
        dialect = csv.excel
        dialect.delimiter = ';'
    for row in csv.DictReader(io.StringIO(text), dialect=dialect):
        yield {str(k).strip(): (v.strip() if isinstance(v,str) else v) for k,v in row.items()}

def _get(row: dict[str,str], *names: str) -> str | None:
    norm = {k.upper().strip().replace(' ','_'): v for k,v in row.items()}
    for name in names:
        v = norm.get(name.upper().strip().replace(' ','_'))
        if v not in (None,''):
            return v
    return None

def _ticker_like(value: str | None) -> bool:
    if not value: return False
    v = value.strip().upper()
    return 3 <= len(v) <= 12 and v.replace('-','').isalnum()

def parse_fca_zip(path: str | Path) -> list[TickerMapping]:
    out=[]
    with zipfile.ZipFile(path) as zf:
        for member in zf.namelist():
            low=member.lower()
            if 'valor_mobiliario' not in low or not low.endswith('.csv'):
                continue
            with zf.open(member) as fh:
                for row in _read_csv(fh.read()):
                    ticker=_get(row,'CODIGO_NEGOCIACAO','CODIGO_NEGOCIACAO_ATIVO','CD_NEGOCIACAO','TICKER','CODIGO')
                    if not _ticker_like(ticker):
                        continue
                    out.append(TickerMapping(
                        ticker=ticker.upper(),
                        cvm_code=_get(row,'CD_CVM','CODIGO_CVM'),
                        company_name=_get(row,'DENOM_CIA','DENOM_SOCIAL','NOME_EMPRESA'),
                        cnpj=_get(row,'CNPJ_CIA','CNPJ'),
                        source_file=member,
                        raw=row,
                    ))
    return out
