# v1.5 — PostgreSQL + API

## Objetivo
Transformar o motor financeiro em um serviço consultável, sem ainda expor login/assinatura ao usuário final.

## Banco
PostgreSQL/Supabase é o alvo. O schema existente permanece a fonte de verdade e `sql/v1_5_api.sql` adiciona índices e a view operacional `v_latest_company_metrics`.

## API
- `GET /health`
- `POST /calculate` — cálculo isolado, útil para testes.
- `GET /api/ativos` — universo ativo com status de qualidade.
- `GET /api/ativos/{ticker}` — empresa + métricas + histórico de preços + eventos corporativos.
- `GET /api/ranking/graham`
- `GET /api/ranking/bazin`
- `GET /api/ranking/gordon`
- `GET /api/ranking/projective`
- `GET /api/ranking/quality`
- `GET /api/ranking/dy`
- `GET /api/radar`
- `GET /api/qualidade-dados`

## Configuração
Defina `DATABASE_URL` ou `SUPABASE_DB_URL` com uma string PostgreSQL. O código usa `psycopg` e é compatível com PostgreSQL gerenciado.

## Regra importante
A API não cria dados financeiros. Ela consulta dados persistidos e calculados pelo pipeline. Isso mantém a separação entre coleta, validação, cálculo e apresentação.

## Próximo marco
Depois de validar a API contra um banco PostgreSQL real:
1. ingestão CVM real;
2. carga dos 93 ativos;
3. execução EOD;
4. dashboard web;
5. autenticação e assinaturas.
