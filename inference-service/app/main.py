import os
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.getenv("MODEL_PATH", os.path.join(BASE_DIR, "model", "model.joblib"))
MODEL_VERSION = os.getenv("MODEL_VERSION", "1.0.0")

model = joblib.load(MODEL_PATH)
app = FastAPI(title="Inference Service")


class Features(BaseModel):
    features: list[float]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/model-info")
def model_info():
    return {
        "model": type(model).__name__,
        "version": MODEL_VERSION,
        "n_features": int(model.n_features_in_),
        "classes": [int(c) for c in model.classes_],
    }


@app.post("/predict")
def predict(data: Features):
    if len(data.features) != model.n_features_in_:
        raise HTTPException(
            status_code=422,
            detail=f"Expected {model.n_features_in_} features, got {len(data.features)}",
        )
    prediction = model.predict([data.features])[0]
    return {"prediction": int(prediction)}