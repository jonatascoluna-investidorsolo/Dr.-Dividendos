-- v1.5 — API / PostgreSQL hardening
-- Compatível com PostgreSQL/Supabase.

create index if not exists idx_companies_active_ticker on companies(is_active, ticker);
create index if not exists idx_metrics_ranking_quality on calculated_metrics(calculation_date desc, quality_score desc);
create index if not exists idx_metrics_ranking_dy on calculated_metrics(calculation_date desc, dividend_yield desc);
create index if not exists idx_metrics_ranking_graham on calculated_metrics(calculation_date desc, graham_upside desc);
create index if not exists idx_metrics_ranking_bazin on calculated_metrics(calculation_date desc, bazin_margin desc);
create index if not exists idx_metrics_ranking_gordon on calculated_metrics(calculation_date desc, gordon_upside desc);
create index if not exists idx_metrics_ranking_projective on calculated_metrics(calculation_date desc, projective_upside desc);

comment on table companies is 'Cadastro mestre de emissores/ativos do Doutor dos Dividendos.';
comment on table financial_statements is 'DFP/ITR normalizados com versionamento e rastreabilidade.';
comment on table market_prices is 'Cotações EOD por fonte, sem sobrescrever histórico de outra fonte.';
comment on table corporate_actions is 'Eventos corporativos/proventos com fingerprint e versionamento.';
comment on table calculated_metrics is 'Snapshot imutável dos cálculos por data e versão da metodologia.';

-- View operacional para a API: uma linha por empresa com a métrica mais recente.
create or replace view v_latest_company_metrics as
select distinct on (cm.company_id)
  cm.*, c.ticker, c.company_name, c.sector, c.segment, c.is_financial,
  c.last_data_quality_status
from calculated_metrics cm
join companies c on c.id = cm.company_id
where c.is_active = true
order by cm.company_id, cm.calculation_date desc, cm.created_at desc;
