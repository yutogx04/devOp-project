import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient
from app import main

client = TestClient(main.app)


class FakeResponse:
    status_code = 200

    def json(self):
        return {"prediction": 1}


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_predict_is_stored(monkeypatch):
    monkeypatch.setattr(main.httpx, "post", lambda *a, **k: FakeResponse())
    r = client.post("/predict", json={"features": [5.1, 3.5, 1.4, 0.2]})
    assert r.status_code == 200
    assert r.json()["prediction"] == 1

    history = client.get("/predictions")
    assert history.status_code == 200
    assert len(history.json()) >= 1


def test_inference_service_down(monkeypatch):
    def boom(*a, **k):
        raise main.httpx.ConnectError("down")

    monkeypatch.setattr(main.httpx, "post", boom)
    r = client.post("/predict", json={"features": [1.0, 2.0, 3.0, 4.0]})
    assert r.status_code == 503
