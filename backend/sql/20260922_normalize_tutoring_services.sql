-- Normalized tutoring-service catalogue.
-- Run once against the current PostgreSQL/Supabase database after pulling this commit.
CREATE TYPE service_kind AS ENUM ('GROUP_TUITION','ONE_ON_ONE','READING_WEEK','SUPPLEMENTARY');
CREATE TYPE billing_period AS ENUM ('MODULE','PACKAGE','WEEK');

CREATE TABLE services (
  id UUID PRIMARY KEY,
  code VARCHAR(40) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  kind service_kind NOT NULL UNIQUE,
  description TEXT,
  active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE module_offerings (
  id UUID PRIMARY KEY,
  module_id UUID NOT NULL REFERENCES modules(id),
  service_id UUID NOT NULL REFERENCES services(id),
  price NUMERIC(10,2) NOT NULL CHECK (price > 0),
  billing_period billing_period NOT NULL,
  sessions_per_week INTEGER CHECK (sessions_per_week IS NULL OR sessions_per_week > 0),
  session_minutes INTEGER CHECK (session_minutes IS NULL OR session_minutes > 0),
  active BOOLEAN NOT NULL DEFAULT TRUE,
  CONSTRAINT uq_module_service_offering UNIQUE(module_id,service_id)
);

CREATE INDEX ix_module_offerings_module_id ON module_offerings(module_id);
CREATE INDEX ix_module_offerings_service_id ON module_offerings(service_id);

INSERT INTO services(id,code,name,kind,description)
VALUES
(gen_random_uuid(),'GROUP','Group Tuition','GROUP_TUITION','Structured semester tuition with other students.'),
(gen_random_uuid(),'ONE_ON_ONE','One-on-One','ONE_ON_ONE','Personal tutoring focused on the individual student.'),
(gen_random_uuid(),'READING_WEEK','Reading Week Revision','READING_WEEK','Dedicated exam revision offered during reading week.'),
(gen_random_uuid(),'SUPP','Supplementary Exam Prep','SUPPLEMENTARY','Dedicated support for supplementary examinations.');

-- Existing modules receive the agreed catalogue.
INSERT INTO module_offerings(id,module_id,service_id,price,billing_period,sessions_per_week,session_minutes,active)
SELECT gen_random_uuid(),m.id,s.id,
  CASE s.kind
    WHEN 'GROUP_TUITION' THEN 150
    WHEN 'ONE_ON_ONE' THEN 200
    WHEN 'READING_WEEK' THEN 100
    WHEN 'SUPPLEMENTARY' THEN 250
  END,
  CASE s.kind WHEN 'READING_WEEK' THEN 'WEEK'::billing_period ELSE 'MODULE'::billing_period END,
  CASE s.kind WHEN 'GROUP_TUITION' THEN 3 ELSE NULL END,
  CASE s.kind WHEN 'GROUP_TUITION' THEN 60 ELSE NULL END,
  TRUE
FROM modules m CROSS JOIN services s
ON CONFLICT (module_id,service_id) DO NOTHING;
