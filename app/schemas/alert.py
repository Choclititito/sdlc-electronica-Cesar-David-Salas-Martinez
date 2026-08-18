from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class AlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    sensor_id: str
    reading_id: int
    value: float
    threshold_breached: Literal["min", "max"]
    message: str
    created_at: datetime
