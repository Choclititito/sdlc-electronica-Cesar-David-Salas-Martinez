from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator
from app.schemas.physics import SensorType, UNIT_TO_TYPE


class SensorIn(BaseModel):
    sensor_id: str = Field(..., examples=["TEMP-01"])
    sensor_type: SensorType
    unit: str = Field(..., examples=["C"])

    @field_validator("unit")
    @classmethod
    def unit_must_be_known(cls, v: str) -> str:
        if v not in UNIT_TO_TYPE:
            raise ValueError(f"Unidad desconocida: '{v}'")
        return v

    @model_validator(mode="after")
    def unit_must_match_type(self) -> "SensorIn":
        expected = UNIT_TO_TYPE[self.unit]
        if expected != self.sensor_type:
            raise ValueError(
                f"La unidad '{self.unit}' corresponde a '{expected.value}', no a '{self.sensor_type.value}'"
            )
        return self


class SensorOut(SensorIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool
    created_at: datetime


class SensorUpdate(BaseModel):
    sensor_type: SensorType | None = None
    unit: str | None = None