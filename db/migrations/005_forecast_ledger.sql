-- v0.7 immutable forecast registration/resolution ledger.
CREATE TABLE IF NOT EXISTS registered_forecast (
  id text PRIMARY KEY,
  registered_at timestamptz NOT NULL,
  cutoff date NOT NULL,
  target_date date NOT NULL CHECK (target_date > cutoff),
  target text NOT NULL,
  kind text NOT NULL CHECK (kind IN ('binary','positive_continuous')),
  prediction double precision NOT NULL,
  model_spec jsonb NOT NULL,
  evidence_ids text[] NOT NULL DEFAULT '{}',
  artifact_hash text NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS forecast_resolution (
  forecast_id text PRIMARY KEY REFERENCES registered_forecast(id),
  resolved_at timestamptz NOT NULL,
  actual double precision NOT NULL,
  score jsonb NOT NULL
);
