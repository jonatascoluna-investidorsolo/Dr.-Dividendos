# API ↔ página individual — v2.2

A página `frontend/empresa.html` passou a operar em modo **API-first**.

## Uso

- `empresa.html?ticker=ITUB4&api=http://localhost:8000`
- ou configure `localStorage.DD_API_BASE`.
- sem API, a tela cai automaticamente para dados demonstrativos.

## Contrato mínimo

`GET /api/ativos/{ticker}` deve retornar:

- `company_name`, `sector`, `last_data_quality_status`;
- `latest_metrics` com `lpa`, `vpa`, `dpa`, `dividend_yield`, `pe_current`, `quality_score`;
- `latest_quote`;
- `financial_history` com período, divulgação, versão e valores contábeis;
- `corporate_actions` com valores ajustados;
- `quality_gate`.

A página não trata o fallback demonstrativo como dado de produção.
