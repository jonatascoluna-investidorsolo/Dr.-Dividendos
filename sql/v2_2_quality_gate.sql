-- Quality Gate is computed by the application layer to keep the rules explicit
-- and versioned. These columns make the decision auditable when persisted.
alter table companies add column if not exists quality_gate_status text;
alter table companies add column if not exists ranking_eligible boolean not null default false;
alter table companies add column if not exists quality_gate_score integer;
alter table companies add column if not exists quality_gate_flags jsonb;
create index if not exists idx_companies_ranking_eligible on companies(ranking_eligible) where ranking_eligible = true;
