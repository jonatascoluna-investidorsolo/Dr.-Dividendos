# v1.6 — Validação do universo real

Objetivo: validar os 93 ativos da planilha contra o FCA oficial da CVM antes de alimentar o motor financeiro com dados reais.

## Regra de identidade

`ticker -> CVM code -> CNPJ -> companhia -> período/documento`

O ticker não é tratado como identidade contábil suficiente. O histórico deve preservar a companhia e a versão do documento.

## Status

- `MATCH`: ticker localizado de forma unívoca no FCA.
- `MISSING`: não localizado no arquivo FCA fornecido.
- `REVIEW`: mais de um registro encontrado; exige desambiguação temporal.
- `SPECIAL_HANDLING`: provável BDR ou instrumento que não deve ser forçado para uma companhia brasileira da CVM.

## Execução

```bash
python scripts_validate_universe.py --excel /caminho/Planilha_Doutor_dos_Dividendos_v2.xlsx
```

Ou, para trabalhar offline com um arquivo FCA previamente baixado:

```bash
python scripts_validate_universe.py \
  --excel /caminho/Planilha_Doutor_dos_Dividendos_v2.xlsx \
  --fca data/raw/fca_cia_aberta_2026.zip
```

O resultado é salvo em `artifacts/universe_validation.csv`.

## Fontes oficiais

- DFP: https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/
- ITR: https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/
- FCA: https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/FCA/DADOS/
- Cadastro: https://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/

A CVM informa que DFP/ITR são atualizados com reapresentações e mantém metadados oficiais. O sistema não deve sobrescrever silenciosamente versões anteriores.

## Limitação do ambiente de desenvolvimento

O ambiente desta execução não conseguiu resolver o DNS de `dados.cvm.gov.br`; portanto, os arquivos oficiais não foram baixados aqui. O código de ingestão está preparado para execução em ambiente com acesso externo ou usando os arquivos oficiais previamente baixados.
