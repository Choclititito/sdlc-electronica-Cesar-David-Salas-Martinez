from typing import Protocol
from sqlalchemy.orm import Session
from app.models.sensor import SensorModel


class SensorRepository(Protocol):
    def add(self, sensor_id: str, sensor_type: str, unit: str) -> SensorModel: ...
    def get_by_sensor_id(self, sensor_id: str) -> SensorModel | None: ...
    def list_all(self, limit: int, offset: int) -> list[SensorModel]: ...
    def update(self, sensor_id: str, sensor_type: str | None, unit: str | None) -> SensorModel | None: ...
    def deactivate(self, sensor_id: str) -> SensorModel | None: ...


class SqlAlchemySensorRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, sensor_id: str, sensor_type: str, unit: str) -> SensorModel:
        sensor = SensorModel(sensor_id=sensor_id, sensor_type=sensor_type, unit=unit)
        self._session.add(sensor)
        self._session.commit()
        self._session.refresh(sensor)
        return sensor

    def get_by_sensor_id(self, sensor_id: str) -> SensorModel | None:
        return (
            self._session.query(SensorModel)
            .filter(SensorModel.sensor_id == sensor_id)
            .first()
        )

    def list_all(self, limit: int, offset: int) -> list[SensorModel]:
        return (
            self._session.query(SensorModel)
            .filter(SensorModel.is_active.is_(True))
            .offset(offset)
            .limit(limit)
            .all()
        )

    def update(self, sensor_id: str, sensor_type: str | None, unit: str | None) -> SensorModel | None:
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

    def deactivate(self, sensor_id: str) -> SensorModel | None:
        sensor = self.get_by_sensor_id(sensor_id)
        if sensor is None:
            return None
        sensor.is_active = False
        self._session.commit()
        self._session.refresh(sensor)
        return sensor