# v1.3 — Ingestão real e readiness

## Objetivo
Transformar o pipeline v1.2 em uma fronteira de ingestão executável, mantendo o motor determinístico e isolando falhas por ativo.

## Fontes oficiais
- CVM DFP: demonstrações anuais e reapresentações.
- CVM ITR: demonstrações trimestrais.
- CVM FCA/Cadastro: identidade e relacionamento com valores mobiliários.
- B3 UP2DATA: eventos corporativos e dados de fechamento, mediante acesso contratado.
- Yahoo: fallback/validação de mercado, não fonte contábil.

## Regra crítica
Se uma fonte não estiver acessível, o sistema não transforma a ausência em zero nem inventa um valor. O ativo fica em `REVIEW` e a execução registra a falha da fonte.

## Execução
```bash
python scripts/check_sources.py
pytest -q
```

O health-check testa apenas conectividade do endpoint. Ele não equivale à validação dos dados. A validação de conteúdo exige download dos arquivos e processamento dos dados reais.

## Estado desta build
O ambiente de construção não possui resolução DNS para os endpoints externos. Portanto, a arquitetura foi preparada e testada localmente, mas nenhum valor real de CVM/B3 foi fabricado para mascarar essa limitação.
