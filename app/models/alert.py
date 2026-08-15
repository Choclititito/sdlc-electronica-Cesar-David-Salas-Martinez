"""models/alert.py
Registro de anomalias detectadas al recibir una lectura fuera de umbral."""

from datetime import datetime, timezone

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class AlertModel(Base):
    __tablename__ = "alerts"
    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[str] = mapped_column(
        ForeignKey("sensors.sensor_id", name="fk_alerts_sensor_id"), index=True
    )
    reading_id: Mapped[int] = mapped_column(
        ForeignKey("readings.id", name="fk_alerts_reading_id")
    )
    value: Mapped[float]
    threshold_breached: Mapped[str]  # "min" o "max"
    message: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), index=True
    )
