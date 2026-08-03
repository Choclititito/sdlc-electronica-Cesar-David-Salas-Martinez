""" readings_repository.py
    Dia 4        """

#Importacion de los modulos necesarios
from typing import Protocol
from datetime import datetime
from sqlalchemy.orm import Session
#Importamos el modelo de lectura de la base de datos
from app.models.reading import ReadingModel

# clase para poder leer y obtener datos
class ReadingRepository(Protocol):
    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel: ...
    def get_by_id(self, reading_id: int) -> ReadingModel | None: ...
    def list_for_sensor(
        self, sensor_id: str, limit: int, offset: int,
        date_from: datetime | None, date_to: datetime | None,
    ) -> list[ReadingModel]: ...
    def update(self, reading_id: int, value: float | None, unit: str | None) -> ReadingModel | None: ...
    def deactivate(self, reading_id: int) -> ReadingModel | None: ...

# Clase SqlAlchemyReadingRepository que implementa la interfaz ReadingRepository
class SqlAlchemyReadingRepository:
    def __init__(self, session: Session) -> None:
        self._session = session
    # Implementacion de los metodos de la interfaz ReadingRepository
    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        reading = ReadingModel(sensor_id=sensor_id, value=value, unit=unit)
        self._session.add(reading)
        self._session.commit()
        self._session.refresh(reading)
        return reading
    # Implementacion del metodo get_by_id que obtiene una lectura por su id
    def get_by_id(self, reading_id: int) -> ReadingModel | None:
        return self._session.get(ReadingModel, reading_id)
    # el como ver todas las lecturas de un sensor con paginacion y filtrado por fecha
    def list_for_sensor(
        self, sensor_id: str, limit: int, offset: int,
        date_from: datetime | None, date_to: datetime | None,
    ) -> list[ReadingModel]:
        query = self._session.query(ReadingModel).filter(
            ReadingModel.sensor_id == sensor_id,
            ReadingModel.is_active.is_(True),
        )
        if date_from is not None:
            query = query.filter(ReadingModel.created_at >= date_from)
        if date_to is not None:
            query = query.filter(ReadingModel.created_at <= date_to)
        return query.order_by(ReadingModel.created_at).offset(offset).limit(limit).all()
    # El como actualizar una lectura por su id
    def update(self, reading_id: int, value: float | None, unit: str | None) -> ReadingModel | None:
        reading = self.get_by_id(reading_id)
        if reading is None:
            return None
        if value is not None:
            reading.value = value
        if unit is not None:
            reading.unit = unit
        self._session.commit()
        self._session.refresh(reading)
        return reading
    #El como desactivar una lectura por su id
    def deactivate(self, reading_id: int) -> ReadingModel | None:
        reading = self.get_by_id(reading_id)
        if reading is None:
            return None
        reading.is_active = False
        self._session.commit()
        self._session.refresh(reading)
        return reading