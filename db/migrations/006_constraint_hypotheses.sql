-- Radiant v0.11: keep constraint hypotheses separate from evidence and identified effects.
CREATE TABLE IF NOT EXISTS constraint_hypothesis (
  hypothesis_id TEXT PRIMARY KEY,
  system_id TEXT NOT NULL,
  constraint_name TEXT NOT NULL,
  causal_claim TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('candidate','supported_directionally','identified','rejected')),
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS constraint_evidence_binding (
  hypothesis_id TEXT NOT NULL,
  evidence_id TEXT NOT NULL,
  relation TEXT NOT NULL CHECK(relation IN ('supports_presence','supports_direction','quantifies_effect','contradicts')),
  note TEXT,
  PRIMARY KEY(hypothesis_id,evidence_id,relation),
  FOREIGN KEY(hypothesis_id) REFERENCES constraint_hypothesis(hypothesis_id)
);
CREATE TABLE IF NOT EXISTS capacity_addition (
  addition_id TEXT PRIMARY KEY,
  system_id TEXT NOT NULL,
  units_per_year REAL,
  available_year INTEGER,
  product_definition TEXT NOT NULL,
  evidence_id TEXT NOT NULL,
  evidence_level TEXT NOT NULL,
  CHECK(units_per_year IS NULL OR units_per_year >= 0)
);
