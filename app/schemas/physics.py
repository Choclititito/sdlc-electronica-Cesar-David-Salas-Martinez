from enum import Enum


class SensorType(str, Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    PRESSURE = "pressure"
    VOLTAGE = "voltage"


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