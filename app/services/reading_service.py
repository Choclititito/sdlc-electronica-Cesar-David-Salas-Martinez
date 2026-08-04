""" services/reading_service.py
    Dia 5 arreglo - se quita SensorMismatchError, ya no aplica"""

# Importaciones
from datetime import datetime
from app.repositories.reading_repository import ReadingRepository
from app.models.reading import ReadingModel
from app.services.exceptions import ReadingNotFoundError, InvalidDateRangeError

ABSOLUTE_ZERO_C = -273.15

# Lógica de negocio de lecturas. Depende de la abstracción del repositorio (DIP)
class ReadingService:
    def __init__(self, repo: ReadingRepository) -> None:
        self._repo = repo

    def record_for_sensor(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        # Regla de negocio: nada por debajo del cero absoluto
        if value < ABSOLUTE_ZERO_C:
            raise ValueError("Temperatura por debajo del cero absoluto")
        return self._repo.add(sensor_id, value, unit)

    def history(
        self, sensor_id: str, limit: int, offset: int,
        date_from: datetime | None, date_to: datetime | None,
    ) -> list[ReadingModel]:
        # Regla de negocio: el rango de fechas debe tener sentido
        if date_from is not None and date_to is not None and date_from > date_to:
            raise InvalidDateRangeError("'from' no puede ser posterior a 'to'")
        return self._repo.list_for_sensor(sensor_id, limit, offset, date_from, date_to)

    def get(self, reading_id: int) -> ReadingModel:
        reading = self._repo.get_by_id(reading_id)
        if reading is None:
            raise ReadingNotFoundError(f"Lectura {reading_id} no encontrada")
        return reading

    def update_partial(self, reading_id: int, value: float | None, unit: str | None) -> ReadingModel:
        if value is not None and value < ABSOLUTE_ZERO_C:
            raise ValueError("Temperatura por debajo del cero absoluto")
        reading = self._repo.update(reading_id, value, unit)
        if reading is None:
            raise ReadingNotFoundError(f"Lectura {reading_id} no encontrada")
        return reading

    def deactivate(self, reading_id: int) -> ReadingModel:
        reading = self._repo.deactivate(reading_id)
        if reading is None:
            raise ReadingNotFoundError(f"Lectura {reading_id} no encontrada")
        return reading