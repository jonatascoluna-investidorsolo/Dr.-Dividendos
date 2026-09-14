create extension if not exists pgcrypto;

create table if not exists companies (
  id uuid primary key default gen_random_uuid(),
  ticker text not null unique,
  company_name text not null,
  sector text,
  segment text,
  cvm_code text,
  cnpj text,
  is_financial boolean not null default false,
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists financial_statements (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id),
  document_type text not null check (document_type in ('DFP','ITR')),
  reference_period date not null,
  disclosure_date date,
  version integer not null default 1,
  source text not null,
  source_document_id text,
  net_income numeric,
  attributable_net_income numeric,
  equity_attributable_common numeric,
  cash_and_equivalents numeric,
  financial_debt numeric,
  ebitda numeric,
  shares_outstanding numeric,
  raw_payload jsonb,
  collected_at timestamptz not null default now(),
  unique(company_id, document_type, reference_period, version)
);

create table if not exists market_prices (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id),
  price_date date not null,
  close numeric not null,
  open numeric,
  high numeric,
  low numeric,
  volume numeric,
  source text not null,
  collected_at timestamptz not null default now(),
  unique(company_id, price_date, source)
);

create table if not exists corporate_actions (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id),
  action_type text not null,
  amount_per_share numeric,
  announcement_date date,
  ex_date date,
  record_date date,
  payment_date date,
  status text not null default 'VALID',
  source text not null,
  source_event_id text,
  raw_payload jsonb,
  collected_at timestamptz not null default now()
);

create table if not exists methodology_parameters (
  id uuid primary key default gen_random_uuid(),
  parameter_key text not null unique,
  parameter_value numeric not null,
  effective_from timestamptz not null default now(),
  changed_by text,
  notes text
);

create table if not exists calculated_metrics (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id),
  calculation_date date not null,
  lpa numeric,
  vpa numeric,
  dpa numeric,
  dividend_yield numeric,
  pe_current numeric,
  pb_current numeric,
  graham_value numeric,
  graham_upside numeric,
  bazin_ceiling numeric,
  bazin_margin numeric,
  applied_growth numeric,
  gordon_value numeric,
  gordon_upside numeric,
  projected_lpa numeric,
  projected_dpa numeric,
  projective_ceiling numeric,
  projective_upside numeric,
  dy_score numeric,
  margin_score numeric,
  debt_score numeric,
  growth_score numeric,
  payout_score numeric,
  quality_score numeric,
  seal text,
  calculation_version text not null,
  created_at timestamptz not null default now(),
  unique(company_id, calculation_date, calculation_version)
);

create table if not exists data_quality_events (
  id uuid primary key default gen_random_uuid(),
  company_id uuid references companies(id),
  field_name text,
  old_value text,
  new_value text,
  reason text,
  source text,
  status text not null default 'PENDING',
  created_at timestamptz not null default now(),
  resolved_at timestamptz
);

create index if not exists idx_financial_company_period on financial_statements(company_id, reference_period desc);
create index if not exists idx_prices_company_date on market_prices(company_id, price_date desc);
create index if not exists idx_actions_company_dates on corporate_actions(company_id, ex_date, payment_date);
create index if not exists idx_metrics_company_date on calculated_metrics(company_id, calculation_date desc);

create table if not exists company_identifiers (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references companies(id),
  identifier_type text not null,
  identifier_value text not null,
  source text not null,
  valid_from date,
  valid_to date,
  unique(identifier_type, identifier_value, source)
);

create table if not exists cvm_ingestion_runs (
  id uuid primary key default gen_random_uuid(),
  document_type text not null check (document_type in ('DFP','ITR','CADASTRO','FCA','IPE')),
  reference_year integer,
  source_url text not null,
  started_at timestamptz not null default now(),
  finished_at timestamptz,
  status text not null default 'RUNNING',
  rows_read integer default 0,
  rows_normalized integer default 0,
  rows_rejected integer default 0,
  error_message text
);

create table if not exists cvm_raw_documents (
  id uuid primary key default gen_random_uuid(),
  ingestion_run_id uuid references cvm_ingestion_runs(id),
  company_id uuid references companies(id),
  document_type text not null,
  reference_period date,
  disclosure_date date,
  version integer not null default 1,
  source_url text not null,
  file_name text,
  content_hash text,
  raw_payload jsonb,
  collected_at timestamptz not null default now(),
  unique(document_type, company_id, reference_period, version, content_hash)
);

create index if not exists idx_company_identifiers_company on company_identifiers(company_id);
create index if not exists idx_cvm_runs_status on cvm_ingestion_runs(status, started_at desc);
create index if not exists idx_cvm_raw_company_period on cvm_raw_documents(company_id, reference_period desc);

-- v1.0: extensões compatíveis para eventos corporativos/proventos
alter table corporate_actions add column if not exists declared_date date;
alter table corporate_actions add column if not exists currency text not null default 'BRL';
alter table corporate_actions add column if not exists gross_amount_per_share numeric;
alter table corporate_actions add column if not exists net_amount_per_share numeric;
alter table corporate_actions add column if not exists adjustment_factor numeric not null default 1.0;
alter table corporate_actions add column if not exists adjusted_amount_per_share numeric;
alter table corporate_actions add column if not exists validation_status text not null default 'VALID';
alter table corporate_actions add column if not exists event_fingerprint text;
alter table corporate_actions add column if not exists event_version integer not null default 1;
create unique index if not exists uq_corporate_actions_source_event on corporate_actions(source, source_event_id) where source_event_id is not null;
create unique index if not exists uq_corporate_actions_fingerprint on corporate_actions(source, event_fingerprint) where source_event_id is null and event_fingerprint is not null;

-- v1.1: mercado/cotações EOD
alter table market_prices add column if not exists adjusted_close numeric;
alter table market_prices add column if not exists currency text not null default 'BRL';
alter table market_prices add column if not exists validation_status text not null default 'VALID';
alter table market_prices add column if not exists quality_score integer not null default 100;
alter table market_prices add column if not exists source_symbol text;
create index if not exists idx_prices_source_date on market_prices(source, price_date desc);

-- v1.4: persistence/audit hardening
alter table companies add column if not exists last_data_quality_status text not null default 'REVIEW';
alter table market_prices add column if not exists provider_timestamp timestamptz;
alter table financial_statements add column if not exists validation_status text not null default 'VALID';
alter table financial_statements add column if not exists content_hash text;
alter table calculated_metrics add column if not exists input_snapshot_hash text;
create index if not exists idx_financial_validation on financial_statements(company_id, validation_status, reference_period desc);
create index if not exists idx_actions_validation on corporate_actions(company_id, validation_status, ex_date desc);
create index if not exists idx_quality_company_created on data_quality_events(company_id, created_at desc);
