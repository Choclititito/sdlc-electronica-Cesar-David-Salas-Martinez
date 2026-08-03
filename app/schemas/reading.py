""" reading.py
    Dia 5
    Codigo para definir los esquemas de lectura de sensores
"""

#Importaciones
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, model_validator
from app.schemas.physics import UNIT_TO_TYPE, PHYSICAL_RANGE

# Definicion de los esquemas de lectura de sensores
class SensorReadingIn(BaseModel):
    sensor_id: str = Field(..., examples=["TEMP-01"])
    value: float
    unit: str = Field(..., examples=["C"])
    # validacion que la unidad es conocida y que el valor esta dentro del rango fisico
    @model_validator(mode="after")
    def validate_physics(self) -> "SensorReadingIn":
        if self.unit not in UNIT_TO_TYPE:
            raise ValueError(f"Unidad desconocida: '{self.unit}'")
        low, high = PHYSICAL_RANGE[self.unit]
        if not (low <= self.value <= high):
            raise ValueError(
                f"Valor {self.value} fuera de rango físico para '{self.unit}' ({low} a {high})"
            )
        return self


# Definicion de los esquemas de salida de lectura de sensores
class SensorReadingOut(SensorReadingIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    is_active: bool

# Definicion de los esquemas de actualizacion de lectura de sensores
class SensorReadingUpdate(BaseModel):
    value: float | None = None
    unit: str | None = None