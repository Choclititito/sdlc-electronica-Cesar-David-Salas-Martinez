""" readings_repository.py
    Dia 3        """

#Importaciones de los modulos
from typing import Protocol
from sqlalchemy.orm import Session

#Importamos el modelo de lectura de la base de datos
from app.models.reading import ReadingModel

#Se crea una clase para definir la interfaz de lectura de la base de datos
class ReadingRepository(Protocol):
    """La 'interfaz de driver': cualquier implementación debe cumplir este contrato."""
    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel: ...
    def list_for_sensor(self, sensor_id: str) -> list[ReadingModel]: ...

#Se hace una clase para poder implementar la interfaz de lectura de la base de datos
class SqlAlchemyReadingRepository:
    """Implementación real: habla con la base de datos de verdad."""
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        reading = ReadingModel(sensor_id=sensor_id, value=value, unit=unit)
        self._session.add(reading)
        self._session.commit()
        self._session.refresh(reading)
        return reading

    def list_for_sensor(self, sensor_id: str) -> list[ReadingModel]:
        return (
            self._session.query(ReadingModel)
            .filter(ReadingModel.sensor_id == sensor_id)
            .all()
        )