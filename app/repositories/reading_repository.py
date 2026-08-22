"""reading_repository.py
Dia 5 arreglo"""

# Importaciones
from datetime import datetime
from typing import Protocol

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.reading import ReadingModel


# Definición de la interfaz del repositorio de lecturas
class ReadingRepository(Protocol):
    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel: ...
    def get_by_id(self, reading_id: int) -> ReadingModel | None: ...
    def list_for_sensor(
        self,
        sensor_id: str,
        limit: int,
        offset: int,
        date_from: datetime | None,
        date_to: datetime | None,
    ) -> list[ReadingModel]: ...
    def update(
        self, reading_id: int, value: float | None, unit: str | None
    ) -> ReadingModel | None: ...
    def deactivate(self, reading_id: int) -> ReadingModel | None: ...
    def get_values_for_stats(
        self, sensor_id: str, date_from: datetime | None, date_to: datetime | None
    ) -> list[float]: ...
    def count_all(self) -> int: ...


# Implementación del repositorio de lecturas usando SQLAlchemy
class SqlAlchemyReadingRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        reading = ReadingModel(sensor_id=sensor_id, value=value, unit=unit)
        self._session.add(reading)
        self._session.commit()
        self._session.refresh(reading)
        return reading

    def get_by_id(self, reading_id: int) -> ReadingModel | None:
        return self._session.get(ReadingModel, reading_id)

    def list_for_sensor(
        self,
        sensor_id: str,
        limit: int,
        offset: int,
        date_from: datetime | None,
        date_to: datetime | None,
    ) -> list[ReadingModel]:
        stmt = select(ReadingModel).where(
            ReadingModel.sensor_id == sensor_id,
            ReadingModel.is_active.is_(True),
        )
        if date_from is not None:
            stmt = stmt.where(ReadingModel.created_at >= date_from)
        if date_to is not None:
            stmt = stmt.where(ReadingModel.created_at <= date_to)
        # Desempate por id: created_at por sí solo no es determinista
        # si dos lecturas comparten el mismo timestamp.
        stmt = (
            stmt.order_by(ReadingModel.created_at, ReadingModel.id)
            .offset(offset)
            .limit(limit)
        )
        return list(self._session.scalars(stmt).all())

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
        self._session.commit()
        self._session.refresh(reading)
        return reading

    def deactivate(self, reading_id: int) -> ReadingModel | None:
        reading = self.get_by_id(reading_id)
        if reading is None:
            return None
        reading.is_active = False
        self._session.commit()
        self._session.refresh(reading)
        return reading

    def get_values_for_stats(
        self, sensor_id: str, date_from: datetime | None, date_to: datetime | None
    ) -> list[float]:
        stmt = select(ReadingModel.value).where(
            ReadingModel.sensor_id == sensor_id, ReadingModel.is_active.is_(True)
        )
        if date_from is not None:
            stmt = stmt.where(ReadingModel.created_at >= date_from)
        if date_to is not None:
            stmt = stmt.where(ReadingModel.created_at <= date_to)
        return list(self._session.scalars(stmt).all())

    def count_all(self) -> int:
        stmt = (
            select(func.count())
            .select_from(ReadingModel)
            .where(ReadingModel.is_active.is_(True))
        )
        return self._session.scalar(stmt) or 0
