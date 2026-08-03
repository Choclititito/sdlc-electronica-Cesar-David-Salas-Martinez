""" physics.py
    Dia 5
    Codigo para definir los tipos de sensores y sus rangos fisicos
"""

#Importacion de enum 
from enum import Enum

# Definimos tipos de sensores 
class SensorType(str, Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    PRESSURE = "pressure"
    VOLTAGE = "voltage"

#Definimos un diccionario que mapea las unidades a los tipos de sensores
UNIT_TO_TYPE: dict[str, SensorType] = {
    "C": SensorType.TEMPERATURE,
    "F": SensorType.TEMPERATURE,
    "K": SensorType.TEMPERATURE,
    "%": SensorType.HUMIDITY,
    "V": SensorType.VOLTAGE,
    "mV": SensorType.VOLTAGE,
    "kPa": SensorType.PRESSURE,
    "hPa": SensorType.PRESSURE,
    "bar": SensorType.PRESSURE,
}
# Definimos un diccionario que mapea las unidades a sus rangos fisicos
PHYSICAL_RANGE: dict[str, tuple[float, float]] = {
    "C": (-273.15, 1000.0),
    "F": (-459.67, 1832.0),
    "K": (0.0, 1273.15),
    "%": (0.0, 100.0),
    "V": (-1000.0, 1000.0),
    "mV": (-1_000_000.0, 1_000_000.0),
    "kPa": (0.0, 1000.0),
    "hPa": (0.0, 10000.0),
    "bar": (0.0, 100.0),
}