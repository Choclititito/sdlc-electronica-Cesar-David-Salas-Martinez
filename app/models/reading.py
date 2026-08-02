from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class ReadingModel(Base):
    __tablename__ = "readings"
    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[str] = mapped_column(ForeignKey("sensors.sensor_id"), index=True)
    value: Mapped[float]
    unit: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, index=True)
    is_active: Mapped[bool] = mapped_column(default=True)