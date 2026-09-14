from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class AccountMapping:
    metric: str
    statement: str
    account_code: str | None = None
    name_contains: tuple[str, ...] = ()
    priority: int = 100
    aggregation: str = "first"
    sign: float = 1.0

# Versioned first-pass registry. Production should prefer exact CD_CONTA mappings
# whenever the CVM metadata/issuer fixtures establish them.
MAPPINGS: tuple[AccountMapping, ...] = (
    AccountMapping("attributable_net_income", "DRE", name_contains=("lucro atribuível aos acionistas da companhia controladora", "lucro (prejuízo) atribuível aos acionistas da companhia controladora"), priority=5),
    AccountMapping("net_income", "DRE", name_contains=("lucro/prejuízo do período", "lucro líquido do período", "lucro (prejuízo) líquido"), priority=10),
    AccountMapping("equity_attributable_common", "BPP", name_contains=("patrimônio líquido atribuível aos acionistas da companhia controladora",), priority=5),
    AccountMapping("cash_and_equivalents", "BPA", name_contains=("caixa e equivalentes de caixa",), priority=5),
    AccountMapping("short_debt", "BPP", name_contains=("empréstimos e financiamentos - circulante",), priority=5),
    AccountMapping("long_debt", "BPP", name_contains=("empréstimos e financiamentos - não circulante",), priority=5),
    AccountMapping("total_debt", "BPP", name_contains=("empréstimos e financiamentos",), priority=20),
    AccountMapping("ebitda", "DRE", name_contains=("ebitda", "lajida"), priority=5),
)

STATEMENT_ALIASES = {"DRE": ("DRE",), "BPA": ("BPA",), "BPP": ("BPP",)}
