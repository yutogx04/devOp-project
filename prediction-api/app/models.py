from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, DateTime, JSON
from app.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    features = Column(JSON, nullable=False)
    prediction = Column(Integer, nullable=False)
    latency_ms = Column(Float)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
