-- ============================================================
-- MLOps Platform – PostgreSQL initialization script
-- Executed once when the postgres container is first created.
-- ============================================================

CREATE TABLE IF NOT EXISTS models (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    version    VARCHAR(50)  NOT NULL,
    n_features INT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (name, version)
);

CREATE TABLE IF NOT EXISTS predictions (
    id            SERIAL PRIMARY KEY,
    model_id      INT REFERENCES models(id),
    features      JSONB NOT NULL,
    prediction    INT,
    latency_ms    FLOAT,
    status        VARCHAR(20) NOT NULL DEFAULT 'success',
    error_message TEXT,
    created_at    TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_predictions_created_at ON predictions (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_predictions_model_id   ON predictions (model_id);

-- Seed the default Iris model
INSERT INTO models (name, version, n_features)
VALUES ('iris_rf', '1.0.0', 4)
ON CONFLICT (name, version) DO NOTHING;
