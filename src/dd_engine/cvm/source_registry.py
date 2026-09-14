from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class SourceRecord:
    name: str
    url: str
    kind: str
    cadence: str
    priority: int

CVM_SOURCES = [
    SourceRecord('CVM DFP', 'https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/', 'fundamentals', 'weekly', 1),
    SourceRecord('CVM ITR', 'https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/', 'fundamentals', 'weekly', 1),
    SourceRecord('CVM FCA', 'https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/FCA/DADOS/', 'security_mapping', 'weekly', 1),
    SourceRecord('CVM Cadastro', 'https://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/', 'company_registry', 'daily', 1),
]

def source_manifest():
    now = datetime.now(timezone.utc).isoformat()
    return [{**r.__dict__, 'checked_at_utc': now} for r in CVM_SOURCES]
