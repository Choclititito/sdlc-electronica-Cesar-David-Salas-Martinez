from dataclasses import dataclass
from enum import Enum, auto
from typing import Protocol
 
class SensorType(Enum):            # enums: como tus #define, pero con tipo
    TEMPERATURE = auto()
    HUMIDITY = auto()
 
@dataclass(frozen=True)            # dataclass inmutable: struct + constructor + igualdad
class Reading:
    sensor_id: str
    value: float
    sensor_type: SensorType
 
class Transport(Protocol):         # Protocol: la interfaz sin herencia forzada
    def send(self, payload: bytes) -> None: ...
 
def to_frame(r: Reading) -> bytes: # funcion pura, facil de testear
    return f"{r.sensor_id}:{r.value:.2f}".encode()

def diff_offset(r: Reading, offset: float) -> str:
    Difference = r.value - offset
    return f"Sensor {r.sensor_id} has a difference of {Difference:.2f}"
