"""Production entrypoint placeholder for daily EOD market ingestion.
Fails closed: no database write is attempted unless SUPABASE_DB_URL exists.
"""
import os
from datetime import datetime, timezone

if not os.getenv('SUPABASE_DB_URL'):
    raise SystemExit('SUPABASE_DB_URL not configured; refusing to write market data')
print('market_update_ready', datetime.now(timezone.utc).isoformat())
