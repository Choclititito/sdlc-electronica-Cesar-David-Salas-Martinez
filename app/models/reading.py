""" models/reading.py
    Dia 5 arreglo"""

# Importaciones
from datetime import datetime, timezone
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base

# Modelo de la tabla "readings" (lecturas de sensores)
class ReadingModel(Base):
    __tablename__ = "readings"
    id: Mapped[int] = mapped_column(primary_key=True)
    # FK hacia sensors.sensor_id: una lectura no puede existir sin su sensor
    sensor_id: Mapped[str] = mapped_column(ForeignKey("sensors.sensor_id"), index=True)
    value: Mapped[float]
    unit: Mapped[str]
    # datetime.now(timezone.utc) en vez de datetime.utcnow() (deprecado)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), index=True
    )
    # Soft delete: True mientras la lectura esté "viva"
    is_active: Mapped[bool] = mapped_column(default=True)