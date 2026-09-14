-- v2.7 automation audit tables. Apply after the core schema.
create table if not exists ingestion_runs (
  id bigserial primary key,
  job_name text not null,
  source text not null,
  started_at timestamptz not null default now(),
  finished_at timestamptz,
  status text not null check (status in ('RUNNING','SUCCEEDED','FAILED','UNREACHABLE')),
  rows_read integer default 0,
  rows_written integer default 0,
  error_message text,
  run_hash text
);

create index if not exists idx_ingestion_runs_source_started
  on ingestion_runs(source, started_at desc);

create table if not exists source_artifacts (
  id bigserial primary key,
  source text not null,
  url text not null,
  collected_at timestamptz not null default now(),
  filename text,
  sha256 text,
  status text not null check (status in ('DOWNLOADED','UNREACHABLE','INVALID','VALIDATED')),
  http_status integer,
  error_message text,
  unique(source, url, sha256)
);

create index if not exists idx_source_artifacts_source_collected
  on source_artifacts(source, collected_at desc);
