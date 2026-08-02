""" reading_service.py
    Dia 4        """

# Importaciones de los modulos necesarios
from datetime import datetime
from app.repositories.reading_repository import ReadingRepository
from app.models.reading import ReadingModel
from app.services.exceptions import (
    ReadingNotFoundError, SensorMismatchError, InvalidDateRangeError,
)

# Definimos una constante para el cero absoluto en grados Celsius
ABSOLUTE_ZERO_C = -273.15

# Clase ReadingService que implementa la logica de negocio para las lecturas
class ReadingService:
    def __init__(self, repo: ReadingRepository) -> None:
        self._repo = repo
    # def para registrar una lectura para un sensor
    def record_for_sensor(
        self, path_sensor_id: str, body_sensor_id: str, value: float, unit: str
    ) -> ReadingModel:
        if path_sensor_id != body_sensor_id:
            raise SensorMismatchError(
                f"sensor_id de la ruta ({path_sensor_id}) no coincide con el del cuerpo ({body_sensor_id})"
            )
        if value < ABSOLUTE_ZERO_C:
            raise ValueError("Temperatura por debajo del cero absoluto")
        return self._repo.add(path_sensor_id, value, unit)
    # def para obtener el historial de lecturas de un sensor
    def history(
        self, sensor_id: str, limit: int, offset: int,
        date_from: datetime | None, date_to: datetime | None,
    ) -> list[ReadingModel]:
        if date_from is not None and date_to is not None and date_from > date_to:
            raise InvalidDateRangeError("'from' no puede ser posterior a 'to'")
        return self._repo.list_for_sensor(sensor_id, limit, offset, date_from, date_to)
    # def para obtener una lectura por su id
    def get(self, reading_id: int) -> ReadingModel:
        reading = self._repo.get_by_id(reading_id)
        if reading is None:
            raise ReadingNotFoundError(f"Lectura {reading_id} no encontrada")
        return reading
    #def para actualizar parcialmente una lectura
    def update_partial(self, reading_id: int, value: float | None, unit: str | None) -> ReadingModel:
        if value is not None and value < ABSOLUTE_ZERO_C:
            raise ValueError("Temperatura por debajo del cero absoluto")
        reading = self._repo.update(reading_id, value, unit)
        if reading is None:
            raise ReadingNotFoundError(f"Lectura {reading_id} no encontrada")
        return reading
    #def para desactivar una lectura
    def deactivate(self, reading_id: int) -> ReadingModel:
        reading = self._repo.deactivate(reading_id)
        if reading is None:
            raise ReadingNotFoundError(f"Lectura {reading_id} no encontrada")
        return reading