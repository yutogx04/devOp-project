from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_model_info():
    r = client.get("/model-info")
    assert r.status_code == 200
    assert r.json()["n_features"] == 4


def test_predict_valid():
    r = client.post("/predict", json={"features": [5.1, 3.5, 1.4, 0.2]})
    assert r.status_code == 200
    assert r.json()["prediction"] in (0, 1, 2)


def test_predict_wrong_feature_count():
    r = client.post("/predict", json={"features": [1.0, 2.0]})
    assert r.status_code == 422