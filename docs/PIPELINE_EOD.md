# Pipeline EOD — v1.2

## Objetivo
Executar um ciclo diário determinístico para os 93 ativos do universo, sem misturar coleta, validação e cálculo.

```text
Universo
  -> Identidade do ativo
  -> Cotação EOD
  -> Eventos corporativos/proventos
  -> Fundamentos CVM
  -> Validação
  -> Motor financeiro
  -> Snapshot auditável
```

## Regras
- A cotação deve ser do próprio pregão solicitado; nunca substituir silenciosamente por outro dia.
- B3/UP2DATA é a fonte preferencial quando disponível/licenciada; Yahoo é fallback/validação.
- Eventos B3 são deduplicados por `source_event_id` ou fingerprint determinístico.
- Eventos cancelados/rejeitados não entram no DPA.
- DPA LTM usa `ex_date` como data de entitlement.
- JCP é mantido em valor bruto para análise de distribuição da companhia.
- Eventos corporativos posteriores a um provento podem exigir ajuste do valor por ação para a base acionária atual.
- Falta de dado produz `REVIEW`/flag; não produz zero artificial.

## Estado
O código está preparado para conectar os adaptadores reais. A execução com arquivos B3/CVM de produção depende de credenciais/acesso de rede no ambiente operacional. Nenhum dado real é fabricado no pacote.
