"""sensor_repository.py
Dia 5
Codigo para definir la interfaz del repositorio de sensores
y su implementacion con SQLAlchemy"""

# Importaciones
from typing import Protocol

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.sensor import SensorModel


# Definimos la interfaz del repositorio de sensores
# Funciona como un contrato que cualquier implementacion de repositorio debe cumplir
class SensorRepository(Protocol):
    def add(self, sensor_id: str, sensor_type: str, unit: str) -> SensorModel: ...
    def get_by_sensor_id(self, sensor_id: str) -> SensorModel | None: ...
    def list_all(self, limit: int, offset: int) -> list[SensorModel]: ...
    def update(
        self, sensor_id: str, sensor_type: str | None, unit: str | None
    ) -> SensorModel | None: ...
    def deactivate(self, sensor_id: str) -> SensorModel | None: ...
    def count_active(self) -> int: ...


# Implementacion del repositorio de sensores usando SQLAlchemy
class SqlAlchemySensorRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    # El como agregar un sensor a la base de datos
    def add(self, sensor_id: str, sensor_type: str, unit: str) -> SensorModel:
        sensor = SensorModel(sensor_id=sensor_id, sensor_type=sensor_type, unit=unit)
        self._session.add(sensor)
        self._session.commit()
        self._session.refresh(sensor)
        return sensor

    # El como obtener un sensor por su id
    def get_by_sensor_id(self, sensor_id: str) -> SensorModel | None:
        stmt = select(SensorModel).where(SensorModel.sensor_id == sensor_id)
        return self._session.scalar(stmt)

    # El como listar todos los sensores activos con paginacion
    def list_all(self, limit: int, offset: int) -> list[SensorModel]:
        stmt = (
            select(SensorModel)
            .where(SensorModel.is_active.is_(True))
            .offset(offset)
            .limit(limit)
        )
        return list(self._session.scalars(stmt).all())

    # El como actualizar un sensor por su id
    def update(
        self, sensor_id: str, sensor_type: str | None, unit: str | None
    ) -> SensorModel | None:
        sensor = self.get_by_sensor_id(sensor_id)
        if sensor is None:
            return None
        if sensor_type is not None:
            sensor.sensor_type = sensor_type
        if unit is not None:
            sensor.unit = unit
        self._session.commit()
        self._session.refresh(sensor)
        return sensor

    # El como desactivar un sensor por su id
    def deactivate(self, sensor_id: str) -> SensorModel | None:
        sensor = self.get_by_sensor_id(sensor_id)
        if sensor is None:
            return None
        sensor.is_active = False
        self._session.commit()
        self._session.refresh(sensor)
        return sensor

    # El como contar sensores activos (para el endpoint de metricas)
    def count_active(self) -> int:
        stmt = select(func.count()).select_from(SensorModel).where(
            SensorModel.is_active.is_(True)
        )
        return self._session.scalar(stmt) or 0