"""models/sensor.py"""

# Importaciones
from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


# Modelo de la tabla "sensors" (catálogo de sensores registrados)
class SensorModel(Base):
    __tablename__ = "sensors"
    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[str] = mapped_column(unique=True, index=True)
    sensor_type: Mapped[str]
    unit: Mapped[str]
    location: Mapped[str | None] = mapped_column(default=None)
    min_threshold: Mapped[float | None] = mapped_column(default=None)
    max_threshold: Mapped[float | None] = mapped_column(default=None)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
