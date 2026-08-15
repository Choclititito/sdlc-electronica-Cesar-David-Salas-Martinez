"""services/reading_service.py
Dia 5 arreglo - se quita SensorMismatchError, ya no aplica"""

# Importaciones
from datetime import datetime

from app.models.reading import ReadingModel
from app.repositories.reading_repository import ReadingRepository
from app.services.exceptions import InvalidDateRangeError, ReadingNotFoundError

# Cero absoluto por unidad soportada
ABSOLUTE_ZERO_BY_UNIT = {
    "C": -273.15,
    "F": -459.67,
    "K": 0.0,
}
DEFAULT_MAX_LIMIT = 500


# Lógica de negocio de lecturas. Depende de la abstracción del repositorio (DIP)
class ReadingService:
    def __init__(self, repo: ReadingRepository) -> None:
        self._repo = repo

    def _validate_absolute_zero(self, value: float, unit: str | None) -> None:
        if unit is None:
            return

        # Normalizar unidad a mayúsculas para evitar problemas de formato
        unit_key = unit.strip().upper()
        
        # Solo aplicar validación de cero absoluto si es una unidad de temperatura conocida
        if unit_key in ABSOLUTE_ZERO_BY_UNIT:
            limit = ABSOLUTE_ZERO_BY_UNIT[unit_key]
            if value < limit:
                raise ValueError(f"Temperatura {value} {unit} por debajo del cero absoluto ({limit} {unit})")

    def record_for_sensor(
        self, sensor_id: str, value: float, unit: str
    ) -> ReadingModel:
        # Regla de negocio: nada por debajo del cero absoluto
        self._validate_absolute_zero(value, unit)
        return self._repo.add(sensor_id, value, unit)

    def history(
        self,
        sensor_id: str,
        limit: int,
        offset: int,
        date_from: datetime | None,
        date_to: datetime | None,
    ) -> list[ReadingModel]:
        # Validar que los parámetros de paginación no sean negativos
        if limit < 0:
            raise ValueError("El límite (limit) no puede ser negativo")
        if offset < 0:
            raise ValueError("El desplazamiento (offset) no puede ser negativo")

        # Regla de negocio: el rango de fechas debe tener sentido
        if date_from is not None and date_to is not None and date_from > date_to:
            raise InvalidDateRangeError("'from' no puede ser posterior a 'to'")
        
        # Defensa en profundidad: evitar límites excesivos que degraden el rendimiento
        safe_limit = min(limit, DEFAULT_MAX_LIMIT) if limit > 0 else DEFAULT_MAX_LIMIT
        return self._repo.list_for_sensor(sensor_id, safe_limit, offset, date_from, date_to)

    def get(self, reading_id: int) -> ReadingModel:
        reading = self._repo.get_by_id(reading_id)
        if reading is None:
            raise ReadingNotFoundError(f"Lectura {reading_id} no encontrada")
        return reading

    def update_partial(
        self, reading_id: int, value: float | None, unit: str | None
    ) -> ReadingModel:
        if value is not None:
            # Si no se provee unidad en el patch, intentamos obtener la lectura existente para validar
            if unit is None:
                existing = self.get(reading_id)
                unit = existing.unit
            self._validate_absolute_zero(value, unit)

        reading = self._repo.update(reading_id, value, unit)
        if reading is None:
            raise ReadingNotFoundError(f"Lectura {reading_id} no encontrada")
        return reading

    def deactivate(self, reading_id: int) -> ReadingModel:
        reading = self._repo.deactivate(reading_id)
        if reading is None:
            raise ReadingNotFoundError(f"Lectura {reading_id} no encontrada")
        return reading
