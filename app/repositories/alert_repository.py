"""repositories/alert_repository.py"""

from typing import Protocol

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.alert import AlertModel


class AlertRepository(Protocol):
    def add(
        self,
        sensor_id: str,
        reading_id: int,
        value: float,
        threshold_breached: str,
        message: str,
    ) -> AlertModel: ...
    def list_for_sensor(self, sensor_id: str) -> list[AlertModel]: ...


class SqlAlchemyAlertRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(
        self,
        sensor_id: str,
        reading_id: int,
        value: float,
        threshold_breached: str,
        message: str,
    ) -> AlertModel:
        alert = AlertModel(
            sensor_id=sensor_id,
            reading_id=reading_id,
            value=value,
            threshold_breached=threshold_breached,
            message=message,
        )
        self._session.add(alert)
        self._session.commit()
        self._session.refresh(alert)
        return alert

    def list_for_sensor(self, sensor_id: str) -> list[AlertModel]:
        stmt = (
            select(AlertModel)
            .where(AlertModel.sensor_id == sensor_id)
            .order_by(AlertModel.created_at.desc())
        )
        return list(self._session.scalars(stmt).all())
