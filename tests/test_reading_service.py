""" test_reading_service.py
    Dia 3        """

#Importaciones de los modulos
import pytest
from dataclasses import dataclass, field
#Importamos el servicio de lectura y el modelo de lectura para poder testearlos
from app.services.reading_service import ReadingService
from app.models.reading import ReadingModel


@dataclass
#Se hace una clase para poder implementar la interfaz de lectura de la base de datos
class FakeReadingRepository:
    """Repositorio en memoria: mismo contrato que ReadingRepository, sin BD real."""
    _readings: list[ReadingModel] = field(default_factory=list)
    _next_id: int = 1

    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        reading = ReadingModel(
            id=self._next_id,
            sensor_id=sensor_id,
            value=value,
            unit=unit,
        )
        self._readings.append(reading)
        self._next_id += 1
        return reading

    def list_for_sensor(self, sensor_id: str) -> list[ReadingModel]:
        return [r for r in self._readings if r.sensor_id == sensor_id]


@pytest.fixture
#Prueba para poder testear el servicio de lectura
def service() -> ReadingService:
    return ReadingService(repo=FakeReadingRepository())

#Prueba para testear que se puede guardar una lectura valida
def test_record_valid_reading_is_saved(service: ReadingService):
    reading = service.record(sensor_id="TEMP-01", value=25.0, unit="C")

    assert reading.sensor_id == "TEMP-01"
    assert reading.value == 25.0
    assert reading.unit == "C"

#Prueba para testear que se puede obtener el historial de lecturas de un sensor
def test_record_below_absolute_zero_raises(service: ReadingService):
    with pytest.raises(ValueError, match="cero absoluto"):
        service.record(sensor_id="TEMP-01", value=-300.0, unit="C")

#Prueba para testear que se puede guardar una lectura en el limite del cero absoluto
def test_record_at_exactly_absolute_zero_is_allowed(service: ReadingService):
    # Caso límite: -273.15 en sí NO debería fallar, solo lo que está por debajo
    reading = service.record(sensor_id="TEMP-01", value=-273.15, unit="C")
    assert reading.value == -273.15

#Prueba para testear que se puede obtener el historial de lecturas de un sensor
def test_history_returns_only_readings_for_that_sensor(service: ReadingService):
    service.record(sensor_id="TEMP-01", value=20.0, unit="C")
    service.record(sensor_id="TEMP-02", value=99.0, unit="C")
    service.record(sensor_id="TEMP-01", value=21.0, unit="C")

    history = service.history("TEMP-01")

    assert len(history) == 2
    assert all(r.sensor_id == "TEMP-01" for r in history)