"""schemas/reading.py
Dia 5 arreglo - sensor_id ya no viaja en el body, solo en la ruta"""

# Importaciones
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, model_validator
from app.schemas.physics import UNIT_TO_TYPE, PHYSICAL_RANGE


# Schema de entrada: lo que el cliente manda al crear una lectura
class SensorReadingIn(BaseModel):
    value: float
    unit: str = Field(..., examples=["C"])

    # Valida que la unidad exista y que el valor tenga sentido físico
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


# Schema de salida: lo que la API devuelve al cliente
class SensorReadingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    sensor_id: str
    value: float
    unit: str
    created_at: datetime
    is_active: bool


# Schema de actualización parcial (PATCH): todos los campos opcionales
class SensorReadingUpdate(BaseModel):
    value: float | None = None
    unit: str | None = None
