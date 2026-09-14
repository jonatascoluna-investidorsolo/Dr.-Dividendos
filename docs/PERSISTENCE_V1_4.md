# Persistência v1.4

## Objetivo
A v1.4 transforma o snapshot calculado em uma camada de persistência histórica e auditável.

## Regras
1. Dados históricos não são apagados para atualizar o presente.
2. Cotações são identificadas por `company_id + price_date + source`.
3. Demonstrações financeiras preservam `reference_period + version` e podem carregar `content_hash`.
4. Métricas são identificadas por `company_id + calculation_date + calculation_version`.
5. Alterações relevantes devem gerar `data_quality_events` em vez de sobrescrever silenciosamente uma informação conflitante.
6. `NULL` significa ausência/não aplicabilidade; zero só é usado quando a fonte realmente informa zero.
7. O plano de persistência é separado da execução SQL para permitir testes e posterior conexão com PostgreSQL/Supabase.

## Snapshot diário
Cada execução EOD deve produzir um snapshot por ativo. O snapshot pode estar `READY` ou `REVIEW`. Um ativo em `REVIEW` continua armazenado, mas não deve ser publicado como dado definitivo sem validação.

## Próxima integração
Conectar este contrato a PostgreSQL/Supabase e implementar transações por ativo, com idempotência e logs de ingestão.
