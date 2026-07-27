"""SensorReading: representa una lectura de temperatura/humedad de un sensor IoT (HU-01)."""
#Importaciones de los datos deseados
from dataclasses import dataclass
from datetime import datetime
from numbers import Real

# Rango físico plausible (no umbrales de anomalía, solo validez del dato en sí)
MIN_TEMPERATURE = -40.0
MAX_TEMPERATURE = 80.0
MIN_HUMIDITY = 0.0
MAX_HUMIDITY = 100.0


class InvalidReadingError(ValueError):
    """Se lanza cuando los datos de la lectura son estructuralmente incorrectos
    (tipo de dato inválido o sensor_id vacío), a diferencia de una lectura
    fuera de rango físico, que es válida como dato pero se marca is_valid()=False."""


@dataclass(frozen=True)
class SensorReading: # Se leen los datos que se reciben del sensor y se validan
    sensor_id: str
    temperature: float
    humidity: float
    timestamp: datetime

    def __post_init__(self): # Validación de los datos de la lectura, con casos de error
        if not self.sensor_id or not isinstance(self.sensor_id, str):
            raise InvalidReadingError("sensor_id no puede estar vacío")
        if not isinstance(self.temperature, Real) or isinstance(self.temperature, bool):
            raise InvalidReadingError(f"temp debe ser numérica {self.temperature!r}")
        if not isinstance(self.humidity, Real) or isinstance(self.humidity, bool):
            raise InvalidReadingError(f"humidity debe ser numérica {self.humidity!r}")
        if not isinstance(self.timestamp, datetime):
            raise InvalidReadingError("timestamp debe ser una instancia de datetime")

    def is_valid(self) -> bool: 
        """Indica si el dato está dentro de un rango físico plausible.
        Una lectura inválida se descarta para el análisis de anomalías (HU-01)."""
        return (
            MIN_TEMPERATURE <= self.temperature <= MAX_TEMPERATURE
            and MIN_HUMIDITY <= self.humidity <= MAX_HUMIDITY
        )

    def to_dict(self) -> dict: # Serializa la lectura a un diccionario, útil para logging o JSON
        return {
            "sensor_id": self.sensor_id,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "timestamp": self.timestamp.isoformat(),
        }
