CREATE TABLE IF NOT EXISTS predictions (
    id          SERIAL PRIMARY KEY,
    model_id    INT REFERENCES models(id),
    input_data  JSONB NOT NULL,
    prediction  JSONB NOT NULL,
    latency_ms  FLOAT,
    status      VARCHAR(20) DEFAULT 'success',
    created_at  TIMESTAMP DEFAULT NOW()
);
CREATE TABLE models (
    id        SERIAL PRIMARY KEY,
    name      VARCHAR(100) NOT NULL,
    version   VARCHAR(50)  NOT NULL,
    UNIQUE (name, version)
);