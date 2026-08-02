from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class SensorModel(Base):
    __tablename__ = "sensors"
    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[str] = mapped_column(unique=True, index=True)
    sensor_type: Mapped[str]
    unit: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)