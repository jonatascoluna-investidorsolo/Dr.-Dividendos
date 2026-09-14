"""CVM ingestion adapters for the Doutor dos Dividendos."""
from .client import CVMClient, CVMEndpoints
from .parser import CVMTableParser, StatementRow
from .normalizer import normalize_statement_rows, infer_financial_metrics

__all__ = [
    "CVMClient", "CVMEndpoints", "CVMTableParser", "StatementRow",
    "normalize_statement_rows", "infer_financial_metrics",
]
