-- v1.2: operational EOD pipeline metadata and quality audit.
ALTER TABLE IF EXISTS market_prices ADD COLUMN IF NOT EXISTS validation_status TEXT DEFAULT 'VALID';
ALTER TABLE IF EXISTS market_prices ADD COLUMN IF NOT EXISTS quality_score INTEGER DEFAULT 100;
ALTER TABLE IF EXISTS market_prices ADD COLUMN IF NOT EXISTS source_symbol TEXT;
ALTER TABLE IF EXISTS market_prices ADD COLUMN IF NOT EXISTS is_adjusted BOOLEAN DEFAULT FALSE;
ALTER TABLE IF EXISTS corporate_actions ADD COLUMN IF NOT EXISTS gross_amount_per_share NUMERIC(20,10);
ALTER TABLE IF EXISTS corporate_actions ADD COLUMN IF NOT EXISTS adjusted_amount_per_share NUMERIC(20,10);
ALTER TABLE IF EXISTS corporate_actions ADD COLUMN IF NOT EXISTS adjustment_factor NUMERIC(20,10) DEFAULT 1;
ALTER TABLE IF EXISTS corporate_actions ADD COLUMN IF NOT EXISTS validation_status TEXT DEFAULT 'VALID';
ALTER TABLE IF EXISTS corporate_actions ADD COLUMN IF NOT EXISTS event_fingerprint TEXT;
ALTER TABLE IF EXISTS corporate_actions ADD COLUMN IF NOT EXISTS declared_date DATE;
ALTER TABLE IF EXISTS corporate_actions ADD COLUMN IF NOT EXISTS currency TEXT DEFAULT 'BRL';

CREATE UNIQUE INDEX IF NOT EXISTS uq_corporate_actions_source_event
  ON corporate_actions(source_event_id)
  WHERE source_event_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS ix_market_prices_ticker_date
  ON market_prices(company_id, price_date);
CREATE INDEX IF NOT EXISTS ix_corporate_actions_ticker_dates
  ON corporate_actions(company_id, ex_date, payment_date);
