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


#EJEMPLOS ---------------------------------------------

#1----
#Codigo para ver la diferencia con el valor deseado
def diff_valordeseado(r: Reading, offset: float) -> str:
    Difference = offset - r.value #Resta el valor para saber que tan cercano o lejano es el valor al offset
    return f"Sensor {r.sensor_id} has a difference of {Difference:.2f}" #Se manda la diferencia

#2----
#Codigo para ver si la lectura se encuentra dentro del rango indicado
def is_reading_valid(r: Reading, min_limit: float, max_limit: float) -> bool:
    #Evalúa si el valor de la lectura está dentro de un rango seguro.
    return min_limit <= r.value <= max_limit

#3----
#Codigo para convertir la lectura de temperatura a Fahrenheit
def convert_to_fahrenheit(r: Reading) -> Reading:
    #Si es temperatura, devuelve una NUEVA lectura en Fahrenheit. Si no, devuelve la original.
    if r.sensor_type != SensorType.TEMPERATURE:
        return r
    
    new_value = (r.value * 9/5) + 32
    # Al ser pura y usar frozen=True, NO modificamos 'r', creamos una nueva instancia
    return Reading(
        sensor_id=r.sensor_id,
        value=new_value,
        sensor_type=r.sensor_type
    )

#4----
#Codigo para hacer un formato de lectura mas amigable
def format_reading_for_display(r: Reading) -> str:
    #Genera una representación amigable para el usuario.
    unit = "°C" if r.sensor_type == SensorType.TEMPERATURE else "%"
    return f"Sensor {r.sensor_id} registró {r.value}{unit}"

#5----
#Codigo para calibrar el sensor
def calibrar(r: Reading, offset: float) -> Reading:
    value_c = r.value + offset #Se le suma el offset
    return Reading(
        sensor_id = r.sensor_id,
        value = value_c,
        sensor_type = r.sensor_type
    )