""" models/reading.py
    Semana 4 Dia 2 - 
    FK con nombre explicito, requerido por batch mode de Alembic en SQLite"""

from datetime import datetime, timezone
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class ReadingModel(Base):
    __tablename__ = "readings"
    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[str] = mapped_column(
        ForeignKey("sensors.sensor_id", name="fk_readings_sensor_id"),
        index=True,
    )
    value: Mapped[float]
    unit: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), index=True
    )
    is_active: Mapped[bool] = mapped_column(default=True)