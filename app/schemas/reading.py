""" reading.py
    Dia 4        """

#Importaciones de los modulos
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

# Aqui se ve como vamos a leer los datos de los sensores
class SensorReadingIn(BaseModel):
    sensor_id: str = Field(..., examples=["TEMP-01"])
    value: float
    unit: str = "C"

# Aqui se ve como se leen los datos de los sensores y se agregan los campos bases
class SensorReadingOut(SensorReadingIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    is_active: bool

# Se actualizan los datos de los sensores, pero solo las lectuas
class SensorReadingUpdate(BaseModel):
    """Todos los campos opcionales: es un PATCH, no un PUT."""
    value: float | None = None
    unit: str | None = None