from app.repositories.sensor_repository import SensorRepository
from app.models.sensor import SensorModel
from app.services.exceptions import SensorNotFoundError, SensorAlreadyExistsError


class SensorService:
    def __init__(self, repo: SensorRepository) -> None:
        self._repo = repo

    def register(self, sensor_id: str, sensor_type: str, unit: str) -> SensorModel:
        if self._repo.get_by_sensor_id(sensor_id) is not None:
            raise SensorAlreadyExistsError(f"El sensor '{sensor_id}' ya existe")
        return self._repo.add(sensor_id, sensor_type, unit)

    def get(self, sensor_id: str) -> SensorModel:
        sensor = self._repo.get_by_sensor_id(sensor_id)
        if sensor is None:
            raise SensorNotFoundError(f"Sensor '{sensor_id}' no encontrado")
        return sensor

    def list(self, limit: int, offset: int) -> list[SensorModel]:
        return self._repo.list_all(limit, offset)

    def update_partial(self, sensor_id: str, sensor_type: str | None, unit: str | None) -> SensorModel:
        sensor = self._repo.update(sensor_id, sensor_type, unit)
        if sensor is None:
            raise SensorNotFoundError(f"Sensor '{sensor_id}' no encontrado")
        return sensor

    def deactivate(self, sensor_id: str) -> SensorModel:
        sensor = self._repo.deactivate(sensor_id)
        if sensor is None:
            raise SensorNotFoundError(f"Sensor '{sensor_id}' no encontrado")
        return sensor