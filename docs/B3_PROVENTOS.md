# B3 — Proventos e eventos corporativos

## Objetivo

A v1.0 cria uma camada canônica para dividendos, JCP e outros pagamentos em dinheiro. A fonte operacional prioritária é a infraestrutura de Eventos Corporativos da B3; a página pública de histórico de proventos é uma camada de conferência.

A B3 informa que o canal Corporate Action do UP2DATA estrutura eventos divulgados pelas companhias e inclui Dividend, Interest on Equity (JCP), stock split, grouping e outros eventos que alteram a base de ações. O Schedule é intradiário e o Life Cycle consolida os eventos ativos. Isso permite separar coleta diária, validação e histórico. 

## Regra de datas

- `announcement_date`: data de divulgação/decisão quando disponível.
- `ex_date`: data usada como padrão para atribuir o provento ao período de direito do acionista e calcular DPA realizado.
- `record_date`: data de registro, quando disponível.
- `payment_date`: data efetiva de pagamento.

O motor preserva todas as datas; não substitui uma pela outra.

## JCP

O valor canônico para análise da política de distribuição é o valor **bruto por ação**. Eventual retenção tributária é uma propriedade do investidor e não deve alterar o payout econômico da companhia. Se a fonte disponibilizar valor líquido, ele pode ser armazenado separadamente sem substituir o bruto.

## Deduplicação

1. `source_event_id` é a chave preferencial.
2. Sem identificador da fonte, usa-se fingerprint determinístico de ticker, tipo, valor e datas.
3. Eventos cancelados/rejeitados não entram no DPA.

## Ajustes por desdobramentos e grupamentos

DPA histórico deve ser comparável na base acionária atual. Se uma empresa fizer desdobramento 2:1 depois de um dividendo de R$1,00/ação, o valor histórico equivalente na base atual é R$0,50/ação.

O motor guarda o valor original e `adjustment_factor`/`adjusted_amount_per_share`, preservando a auditabilidade.

## Payout

Padrão do motor:

`payout = (DPA realizado × ações aplicáveis) / lucro líquido atribuível`

A janela de DPA usa `ex_date`. Se o lucro atribuível for zero/negativo, o payout fica `N/A`, evitando percentuais economicamente sem sentido.

## Integração com a planilha

- `P` DPA projetado continua sendo premissa de payout futuro × LPA.
- O histórico de proventos alimentará DPA realizado, payout histórico e DY histórico.
- O Bazin continuará usando o DPA definido pela metodologia, sem substituir automaticamente a premissa futura pelo histórico.
- Eventos corporativos de ações alimentam a camada de ajustes de quantidade de ações já criada na v0.9.

## Limitação de validação

A arquitetura foi implementada e testada localmente. A execução contra os arquivos estruturados/diários da B3 depende de um ambiente com acesso ao canal de dados correspondente; a existência e a estrutura conceitual das fontes oficiais foram verificadas na documentação pública da B3.
