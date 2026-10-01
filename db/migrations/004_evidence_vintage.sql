-- v0.4: distinguish observation date, source availability, and ingestion time.
-- Strict live replay uses recorded_at. Historical backtests may use source_available_at,
-- but only when availability is independently evidenced (publication/archive timestamp).
ALTER TABLE source ADD COLUMN IF NOT EXISTS source_available_at timestamptz;
ALTER TABLE source ADD COLUMN IF NOT EXISTS retrieved_at timestamptz;
ALTER TABLE source ADD COLUMN IF NOT EXISTS content_sha256 text;
ALTER TABLE source ADD COLUMN IF NOT EXISTS availability_evidence text;

CREATE TABLE IF NOT EXISTS backtest_run (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  domain text NOT NULL,
  metric_id text NOT NULL,
  mode text NOT NULL CHECK (mode IN ('strict_recorded','historical_vintage','retrospective_date_only')),
  cutoff date NOT NULL,
  model_spec jsonb NOT NULL,
  train_observation_ids uuid[] DEFAULT '{}',
  target_observation_ids uuid[] DEFAULT '{}',
  metrics jsonb NOT NULL,
  artifact_hash text NOT NULL,
  created_at timestamptz DEFAULT now()
);
COMMENT ON COLUMN backtest_run.mode IS
 'strict_recorded = only knowledge actually recorded by cutoff; historical_vintage = sources independently proven available by cutoff; retrospective_date_only = exploratory only, cannot pass no-leak gate';
