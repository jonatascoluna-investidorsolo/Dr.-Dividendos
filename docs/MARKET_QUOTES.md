# v1.1 — Cotações EOD

## Objetivo
Atualizar a cotação de fechamento dos ativos do universo diariamente após o encerramento do pregão, mantendo fonte, data, símbolo de origem, validação e qualidade.

## Hierarquia
1. B3 / UP2DATA, quando contratado e disponível.
2. Yahoo Finance como fallback/validação operacional.
3. Google ou outro provedor somente como segunda validação, nunca como substituto silencioso de uma data de pregão ausente.

A B3 define o UP2DATA como plataforma de distribuição de informação de fechamento e dados de referência. O canal de renda variável disponibiliza dados consolidados de mercado e o monitoramento público mostra subcanais como Equities > Reference Price. Portanto, a arquitetura do motor separa o provedor oficial do fallback externo.

## Regra crítica
O motor **não substitui silenciosamente** uma cotação por outra data. Se a data esperada não tiver fechamento válido, o registro fica pendente/REVIEW e a aplicação não recalcula os indicadores como se houvesse uma cotação nova.

## Validação
Cada cotação guarda:
- ticker;
- data do pregão;
- fechamento;
- fonte;
- símbolo utilizado na fonte;
- moeda;
- horário de coleta;
- status de validação;
- score de qualidade.

## Yahoo
Para ações brasileiras, o adaptador converte `PETR4` em `PETR4.SA`. O módulo não depende do Yahoo para a lógica financeira; ele é somente uma fonte intercambiável.

## Próximo passo
Implementar o job diário que percorre os 93 ativos, grava as cotações no PostgreSQL, compara fontes e só então dispara o recálculo dos indicadores.
