# v2.7 — Production automation

## Objective
Move from a validated prototype to repeatable production execution without silently publishing incomplete data.

## Jobs
- `CI`: every push/PR; runs the complete Python test suite.
- `Daily market update`: weekdays after the B3 close window; fetch/validate EOD quotes and recalculate price-dependent metrics.
- `Weekly CVM ingestion`: checks DFP/ITR and new/revised filings, preserves raw artifacts and restatement history.

## Fail-closed rule
Missing credentials, unreachable sources, malformed files, or failed validation must never overwrite the last valid published snapshot.

## Supabase
Supabase Cron/pg_cron is suitable for database-side scheduling and records job execution details. GitHub Actions remains the preferred runner for Python acquisition jobs because secrets, logs and tests stay with the repository.

## Required secrets
- `SUPABASE_DB_URL`
- later: market-data provider credentials if the selected provider requires them.

## Next deployment task
Create the Supabase project, apply schema migrations, add secrets, run CI, then execute ITUB4 in the cloud runner. Only after a successful ITUB4 end-to-end run should the 93-asset universe be enabled.
