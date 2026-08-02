""" reading_service.py
    Dia 3        """

#Importacion del modulo de lectura
from app.repositories.reading_repository import ReadingRepository
#Importamos el modelo de lectura de la base de datos
from app.models.reading import ReadingModel

#Se hace una clase para poder implementar la logica de negocio
class ReadingService:
    """Logica de negocio. Depende de la abstraccion del repositorio (DIP)."""
    def __init__(self, repo: ReadingRepository) -> None:
        self._repo = repo

    def record(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        if value < -273.15:
            raise ValueError("Temperatura por debajo del cero absoluto")
        return self._repo.add(sensor_id, value, unit)

    def history(self, sensor_id: str) -> list[ReadingModel]:
        return self._repo.list_for_sensor(sensor_id)