"""Production entrypoint placeholder for weekly CVM ingestion.
Fails closed when database credentials are absent.
"""
import os
from datetime import datetime, timezone

if not os.getenv('SUPABASE_DB_URL'):
    raise SystemExit('SUPABASE_DB_URL not configured; refusing to publish CVM data')
print('cvm_weekly_ready', datetime.now(timezone.utc).isoformat())
