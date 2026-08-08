"""test_reading_service.py
Dia 5 arreglo"""

# Importaciones
from dataclasses import dataclass, field

import pytest
from app.models.reading import ReadingModel
from app.services.reading_service import ReadingService


# Repositorio fake en memoria: mismo contrato que ReadingRepository, sin BD real
@dataclass
class FakeReadingRepository:
    _readings: list[ReadingModel] = field(default_factory=list)
    _next_id: int = 1

    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        reading = ReadingModel(
            id=self._next_id, sensor_id=sensor_id, value=value, unit=unit
        )
        self._readings.append(reading)
        self._next_id += 1
        return reading

    def list_for_sensor(self, sensor_id: str, **kwargs) -> list[ReadingModel]:
        return [r for r in self._readings if r.sensor_id == sensor_id]


# Fixture: arma un ReadingService nuevo, con fake repo limpio, para cada test
@pytest.fixture
def service() -> ReadingService:
    return ReadingService(repo=FakeReadingRepository())


# Camino feliz: una lectura válida se guarda correctamente
def test_record_valid_reading_is_saved(service: ReadingService):
    reading = service.record_for_sensor(sensor_id="TEMP-01", value=25.0, unit="C")
    assert reading.sensor_id == "TEMP-01"
    assert reading.value == 25.0


# Caso de error: temperatura por debajo del cero absoluto se rechaza
def test_record_below_absolute_zero_raises(service: ReadingService):
    with pytest.raises(ValueError, match="cero absoluto"):
        service.record_for_sensor(sensor_id="TEMP-01", value=-300.0, unit="C")
