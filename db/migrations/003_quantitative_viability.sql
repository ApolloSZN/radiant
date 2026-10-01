-- v0.3: quantitative material/maintenance closure. RAF topology remains separate.
CREATE TABLE IF NOT EXISTS flow_process (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  process_key text NOT NULL UNIQUE,
  system_id uuid,
  capacity double precision,
  capacity_unit text,
  energy_per_flux double precision,
  energy_unit text,
  evidence_source_id uuid,
  recorded_at timestamptz DEFAULT now()
);
CREATE TABLE IF NOT EXISTS flow_coefficient (
  flow_process_id uuid REFERENCES flow_process(id),
  item_key text NOT NULL,
  coefficient double precision NOT NULL, -- output positive, input negative
  unit text NOT NULL,
  PRIMARY KEY(flow_process_id,item_key)
);
CREATE TABLE IF NOT EXISTS maintenance_requirement (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  system_id uuid,
  item_key text NOT NULL,
  rate double precision NOT NULL CHECK(rate >= 0),
  unit text NOT NULL,
  valid_from date,
  valid_to date,
  evidence_source_id uuid,
  recorded_at timestamptz DEFAULT now()
);
CREATE TABLE IF NOT EXISTS import_limit (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  system_id uuid,
  item_key text NOT NULL,
  max_rate double precision NOT NULL CHECK(max_rate >= 0),
  unit text NOT NULL,
  valid_from date,
  valid_to date,
  evidence_source_id uuid,
  recorded_at timestamptz DEFAULT now()
);
CREATE TABLE IF NOT EXISTS viability_run (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  system_id uuid,
  snapshot_at timestamptz NOT NULL,
  raf_core text[] NOT NULL,
  topological_closure boolean NOT NULL,
  material_viability boolean NOT NULL,
  objective double precision,
  fluxes jsonb NOT NULL DEFAULT '{}',
  imports jsonb NOT NULL DEFAULT '{}',
  maintenance_slack jsonb NOT NULL DEFAULT '{}',
  energy_used double precision,
  solver_status text,
  model_hash text,
  created_at timestamptz DEFAULT now()
);
