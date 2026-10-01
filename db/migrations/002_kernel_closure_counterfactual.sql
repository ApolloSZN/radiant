-- v0.2: adaptive-system kernel, catalytic closure, counterfactual runs.
-- Adds the layer beneath capabilities (what a system is) and the layer above
-- (what changes if we intervene). Every row stays bitemporal through the
-- recorded_at / valid_* pattern from 001.

-- ------------------------------------------------------------ kernel
CREATE TABLE adaptive_system (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  scale text NOT NULL CHECK (scale IN
    ('chemical','cell','organism','person','team','lab','firm','market',
     'institution','region','industry','civilization')),
  parent_system_id uuid REFERENCES adaptive_system,
  boundary_definition text NOT NULL,       -- B: operational rule for inside vs outside
  characteristic_timescale_s double precision,
  valid_from date, valid_to date,
  recorded_at timestamptz DEFAULT now()
);

CREATE TABLE state_variable (              -- X, with V bounds
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  system_id uuid NOT NULL REFERENCES adaptive_system,
  metric_id text NOT NULL REFERENCES metric_def,
  viability_low double precision,
  viability_high double precision,
  breach_consequence text,
  observed_by_system boolean DEFAULT false,  -- O
  actuated_by_system boolean DEFAULT false   -- A
);

CREATE TABLE resource_flow (               -- R: what crosses the boundary
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  from_system uuid REFERENCES adaptive_system,   -- null = environment
  to_system uuid REFERENCES adaptive_system,
  item text NOT NULL,
  rate double precision, unit text,
  efficiency real,
  valid_from date, valid_to date,
  recorded_at timestamptz DEFAULT now()
);

-- Operational verdicts, never hand-entered: written only by the kernel tests.
CREATE TABLE property_verdict (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  system_id uuid NOT NULL REFERENCES adaptive_system,
  property text NOT NULL CHECK (property IN
    ('persistent','regulated','self_producing','learning','self_improving','autonomous')),
  passed boolean NOT NULL,
  statistics jsonb NOT NULL,               -- slopes, t-stats, recovery rates, RAF core
  evidence uuid[] NOT NULL,                -- observation ids used
  engine_version text NOT NULL,
  computed_at timestamptz DEFAULT now()
);

-- ------------------------------------------------------------ catalytic closure
CREATE TABLE item (                        -- anything a process consumes, produces or needs
  id text PRIMARY KEY,
  kind text CHECK (kind IN ('molecule','material','energy','tool','skill','data','capital','other'))
);

CREATE TABLE process (                     -- a catalyzed transformation
  id text PRIMARY KEY,
  system_id uuid REFERENCES adaptive_system,
  technology_id uuid REFERENCES technology,
  requires_catalyst boolean DEFAULT true,
  valid_from date, valid_to date,
  recorded_at timestamptz DEFAULT now()
);

CREATE TABLE process_io (
  process_id text REFERENCES process,
  item_id text REFERENCES item,
  role text CHECK (role IN ('input','output','catalyst')),
  quantity double precision,
  source_id uuid REFERENCES source,
  PRIMARY KEY (process_id, item_id, role)
);

CREATE TABLE food_set (                    -- what the environment supplies to a system
  system_id uuid REFERENCES adaptive_system,
  item_id text REFERENCES item,
  valid_from date, valid_to date,
  PRIMARY KEY (system_id, item_id, valid_from)
);

CREATE TABLE raf_result (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  system_id uuid REFERENCES adaptive_system,
  as_of date NOT NULL,                     -- replay date for bitemporal inputs
  core text[] NOT NULL,
  removal_log jsonb NOT NULL,
  engine_version text NOT NULL,
  computed_at timestamptz DEFAULT now()
);

-- ------------------------------------------------------------ transitions and counterfactuals
CREATE TABLE transition_model (            -- executable, versioned; never free text
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  system_id uuid REFERENCES adaptive_system,
  inputs text[] NOT NULL,
  outputs text[] NOT NULL,
  artifact_uri text NOT NULL,              -- code path or model file
  artifact_sha256 text NOT NULL,
  uncertainty jsonb,
  evidence uuid[],
  status epistemic_status DEFAULT 'conjecture'
);

CREATE TABLE intervention (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  kind text NOT NULL CHECK (kind IN
    ('scale_cost','set_rate','cut_supply','add_supply','remove_process')),
  target text NOT NULL,
  value double precision,
  description text
);

CREATE TABLE simulation_run (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  snapshot_as_of timestamptz NOT NULL,     -- replay point: only rows recorded before this
  interventions uuid[] NOT NULL,
  horizon_years double precision NOT NULL,
  draws integer NOT NULL,
  seed bigint NOT NULL,
  model_version text NOT NULL,
  output jsonb NOT NULL,                   -- distributions + causal trace
  result_hash text NOT NULL,               -- gate 4: reproducibility check
  created_at timestamptz DEFAULT now()
);
CREATE UNIQUE INDEX ON simulation_run (snapshot_as_of, interventions, horizon_years, draws, seed, model_version);
