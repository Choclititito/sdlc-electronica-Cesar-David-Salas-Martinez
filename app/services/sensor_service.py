""" sensor_service.py
    Dia 5
    Codigo para definir la logica de negocio de los sensores
    Reglas que le dan sentido a la aplicacion e independientes de su forma HTTP"""

#Importaciones
from app.repositories.sensor_repository import SensorRepository
from app.models.sensor import SensorModel
from app.services.exceptions import SensorNotFoundError, SensorAlreadyExistsError


# Clase SensorService que implementa la logica de negocio de los sensores
class SensorService:
    def __init__(self, repo: SensorRepository) -> None:
        self._repo = repo
        # Registra un nuevo sensor en la base de datos, si ya existe lanza una excepcion
    def register(self, sensor_id: str, sensor_type: str, unit: str) -> SensorModel:
        if self._repo.get_by_sensor_id(sensor_id) is not None:
            raise SensorAlreadyExistsError(f"El sensor '{sensor_id}' ya existe")
        return self._repo.add(sensor_id, sensor_type, unit)
        # Obtiene un sensor por su id, si no existe lanza una excepcion
    def get(self, sensor_id: str) -> SensorModel:
        sensor = self._repo.get_by_sensor_id(sensor_id)
        if sensor is None:
            raise SensorNotFoundError(f"Sensor '{sensor_id}' no encontrado")
        return sensor
        # Lista todos los sensores con paginacion
    def list(self, limit: int, offset: int) -> list[SensorModel]:
        return self._repo.list_all(limit, offset)
        # Actualiza un sensor por su id, si no existe lanza una excepcion
    def update_partial(self, sensor_id: str, sensor_type: str | None, unit: str | None) -> SensorModel:
        sensor = self._repo.update(sensor_id, sensor_type, unit)
        if sensor is None:
            raise SensorNotFoundError(f"Sensor '{sensor_id}' no encontrado")
        return sensor
        # Desactiva un sensor por su id, si no existe lanza una excepcion
    def deactivate(self, sensor_id: str) -> SensorModel:
        sensor = self._repo.deactivate(sensor_id)
        if sensor is None:
            raise SensorNotFoundError(f"Sensor '{sensor_id}' no encontrado")
        return sensor