-- Frontier Capability Map schema v0.1 (unchanged)
-- Enumerations
CREATE TYPE epistemic_status AS ENUM
  ('measured','derived','proven','known_result','conjecture','forecast','disputed','retracted');
CREATE TYPE loop_leg AS ENUM ('read','write','model','verify');
CREATE TYPE source_tier AS ENUM ('T0','T1','T2','T3','T4');
CREATE TYPE curve_form AS ENUM ('wright','moore','logistic','piecewise');

-- Coordinate system
CREATE TABLE substrate (
  id text PRIMARY KEY,                 -- 'dna','proteins','charge',...
  name text NOT NULL,
  scale_min_m double precision,
  scale_max_m double precision
);
CREATE TABLE primitive (
  id text PRIMARY KEY,                 -- 'sense','actuate','verify',...
  leg loop_leg                         -- null for transmit/convert/coordinate
);
CREATE TABLE primitive_instance (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  primitive_id text REFERENCES primitive,
  substrate_id text REFERENCES substrate,
  control_level smallint CHECK (control_level BETWEEN 0 AND 6),
  level_since date,
  level_rule_id text,
  UNIQUE (primitive_id, substrate_id)
);

-- Evidence
CREATE TABLE source (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tier source_tier NOT NULL,
  url text, doi text, title text, published date
);
CREATE TABLE work (
  id uuid PRIMARY KEY REFERENCES source,
  kind text CHECK (kind IN ('paper','preprint','patent','dataset','report')),
  openalex_id text, patent_id text,
  cd_index double precision,
  novelty_z double precision
);
CREATE TABLE metric_def (
  id text PRIMARY KEY,                 -- 'cost_per_op', 'throughput', ...
  unit text NOT NULL,
  better text CHECK (better IN ('up','down')),
  log_scale boolean DEFAULT true
);
CREATE TABLE observation (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  metric_id text REFERENCES metric_def,
  subject_id uuid NOT NULL,            -- primitive_instance, technology or capability
  subject_type text NOT NULL,
  obs_date date NOT NULL,
  log_value double precision,          -- null when outcome = 'null_result'
  log_ci_low double precision,
  log_ci_high double precision,
  outcome text DEFAULT 'value' CHECK (outcome IN ('value','null_result','failed')),
  method text,
  source_id uuid REFERENCES source,
  source_span text,                    -- pointer into the source text
  extraction_confidence real,
  status epistemic_status DEFAULT 'measured',
  recorded_at timestamptz DEFAULT now()
);
CREATE INDEX ON observation (subject_id, metric_id, obs_date);

CREATE TABLE curve (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  subject_id uuid NOT NULL,
  metric_id text REFERENCES metric_def,
  form curve_form NOT NULL,
  params jsonb NOT NULL,               -- {r, w, C0, ...}
  fit_start date, fit_end date,
  residual_sd double precision,
  fitted_at timestamptz DEFAULT now()
);

-- Capability layer
CREATE TABLE technology (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  mechanism text,
  trl smallint CHECK (trl BETWEEN 1 AND 9),
  first_demo date
);
CREATE TABLE capability (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  io_signature text NOT NULL,
  spec jsonb                           -- [{metric_id, bound, direction}]
);
CREATE TABLE loop (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  domain text NOT NULL,
  cycle_time_s double precision,
  closure_index real,
  automation_fraction real,
  tail_index real,
  generator_updates boolean
);
CREATE TABLE constraint_bound (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  kind text CHECK (kind IN ('physical','economic','regulatory')),
  bound_expr text,
  metric_id text REFERENCES metric_def,
  log_bound double precision
);

-- Demand layer
CREATE TABLE use_case (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  description text NOT NULL,
  value_per_unit_usd double precision,
  market_size_usd double precision
);
CREATE TABLE threshold (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  use_case_id uuid REFERENCES use_case,
  metric_id text REFERENCES metric_def,
  log_value double precision NOT NULL,
  derivation text,
  confidence real
);
CREATE TABLE fiction_spec (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  work_title text, artifact text,
  physics_violations text[]
);

-- Dynamics
CREATE TABLE forecast (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  target jsonb NOT NULL,               -- {kind:'crossing', threshold_id} etc.
  distribution jsonb NOT NULL,         -- probability or quantiles
  made_at timestamptz DEFAULT now(),
  resolves_at date,
  outcome jsonb,
  brier real, log_score real
);
CREATE TABLE event (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  kind text CHECK (kind IN ('crossing','level_change','regime_break','first_demo','migration')),
  subject_id uuid, event_date date,
  evidence uuid[]
);
CREATE TABLE candidate (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  input_capabilities uuid[] NOT NULL,
  enabling_event uuid REFERENCES event,
  predicted_capability text,
  value_estimate_usd double precision,
  rank real
);

-- Relations: one bitemporal edge table
CREATE TABLE edge (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  type text NOT NULL,                  -- 'COMPOSED_OF','FEEDS','SUPPORTS',...
  from_id uuid NOT NULL, from_type text NOT NULL,
  to_id uuid NOT NULL,   to_type text NOT NULL,
  props jsonb DEFAULT '{}',            -- cost_share, logic, leg, strength...
  status epistemic_status DEFAULT 'derived',
  valid_from date, valid_to date,      -- true in the world
  recorded_at timestamptz DEFAULT now(),
  retracted_at timestamptz             -- never delete; retract
);
CREATE INDEX ON edge (type, from_id);
CREATE INDEX ON edge (type, to_id);
