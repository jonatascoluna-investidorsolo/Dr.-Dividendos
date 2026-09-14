# Doutor dos Dividendos — v2.4

## Foco
Primeiro runner de ingestão real para uma empresa financeira: ITUB4.

## Fluxo
CVM DFP/ITR → filtro por código CVM → parser → normalização → seleção de período/reapresentação → Quality Gate → banco/API.

O ticker não é usado como identidade contábil: o runner recebe explicitamente o código CVM confirmado no FCA/Cadastro.

## Segurança
- Não aceita correspondência por nome aproximado.
- Não transforma falha de fonte em zero.
- DFP sem snapshot anual válido resulta em REVIEW.
- Dados oficiais devem permanecer acompanhados de período, versão e evidência.

## Execução
```bash
python scripts/run_itub4_live.py --year 2026 --cvm-code <CODIGO_CVM>
```

O código CVM deve ser obtido e confirmado pela camada de identificação oficial antes da execução.

## Situação
O código está preparado para execução em ambiente com acesso aos arquivos oficiais. O ambiente de desenvolvimento atual pode não ter conectividade direta para baixar os ZIPs.
