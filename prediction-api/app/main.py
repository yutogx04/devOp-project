import os
import time
import httpx
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Prediction

INFERENCE_URL = os.getenv("INFERENCE_URL", "http://localhost:8001")

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Prediction API")


class Features(BaseModel):
    features: list[float]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(data: Features, db: Session = Depends(get_db)):
    start = time.perf_counter()
    try:
        resp = httpx.post(
            f"{INFERENCE_URL}/predict",
            json={"features": data.features},
            timeout=10,
        )
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Inference service unavailable")

    if resp.status_code == 422:
        raise HTTPException(status_code=422, detail="Invalid input features")
    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail="Inference service error")

    result = resp.json()["prediction"]
    latency_ms = (time.perf_counter() - start) * 1000

    record = Prediction(features=data.features, prediction=result, latency_ms=latency_ms)
    db.add(record)
    db.commit()
    db.refresh(record)

    return {"id": record.id, "prediction": result, "latency_ms": round(latency_ms, 2)}


@app.get("/predictions")
def list_predictions(limit: int = 50, db: Session = Depends(get_db)):
    rows = db.query(Prediction).order_by(Prediction.id.desc()).limit(limit).all()
    return [
        {
            "id": r.id,
            "features": r.features,
            "prediction": r.prediction,
            "latency_ms": r.latency_ms,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]
