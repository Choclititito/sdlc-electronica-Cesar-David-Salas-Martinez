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

    def get_by_id(self, reading_id: int) -> ReadingModel | None:
        for r in self._readings:
            if r.id == reading_id:
                return r
        return None

    def update(
        self, reading_id: int, value: float | None, unit: str | None
    ) -> ReadingModel | None:
        reading = self.get_by_id(reading_id)
        if reading is None:
            return None
        if value is not None:
            reading.value = value
        if unit is not None:
            reading.unit = unit
        return reading


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


# Caso de éxito: temperatura por debajo del cero absoluto en C pero válida en F
# se acepta
def test_record_fahrenheit_below_celsius_limit_but_above_fahrenheit_limit_is_valid(
    service: ReadingService,
):
    """-300 esta por debajo del cero absoluto en C, pero es valido en F (-459.67)."""
    reading = service.record_for_sensor(sensor_id="TEMP-01", value=-300.0, unit="F")
    assert reading.value == -300.0


# caso de exito: humedad negativa no se valida contra cero absoluto
def test_record_humidity_negative_value_does_not_raise_absolute_zero_error(
    service: ReadingService,
):
    """La validacion de cero absoluto solo aplica a C/F/K, no a otras unidades."""
    reading = service.record_for_sensor(sensor_id="HUM-01", value=-5.0, unit="%")
    assert reading.value == -5.0


# Caso de éxito: temperatura por debajo del cero absoluto en C pero con unidad None se
# acepta
def test_record_with_none_unit_does_not_raise(service: ReadingService):
    reading = service.record_for_sensor(sensor_id="TEMP-01", value=20.0, unit=None)
    assert reading.value == 20.0


# Casos de error: parámetros de paginación de limites negativos se rechazan
def test_history_with_negative_limit_raises_value_error(service: ReadingService):
    with pytest.raises(ValueError, match="limite.*no puede ser negativo|límite"):
        service.history("TEMP-01", limit=-10, offset=0, date_from=None, date_to=None)


# Casos de error: parámetros de paginación de offset negativos se rechazan
def test_history_with_negative_offset_raises_value_error(service: ReadingService):
    with pytest.raises(ValueError, match="desplazamiento|offset"):
        service.history("TEMP-01", limit=50, offset=-5, date_from=None, date_to=None)


# Caso de éxito: actualizar parcialmente una lectura sin unidad valida contra
# la unidad existente
def test_update_partial_without_unit_validates_against_existing_reading_unit(
    service: ReadingService,
):
    created = service.record_for_sensor(sensor_id="TEMP-01", value=20.0, unit="F")
    # Patch solo con value, sin unit -> debe usar la unidad existente (F) para validar
    updated = service.update_partial(created.id, value=-300.0, unit=None)
    assert updated.value == -300.0  # valido en F, no deberia rechazarse
