"""repositories/alert_repository.py"""
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.alert import AlertModel
from app.services.exceptions import AlertCreationError


class AlertRepository(Protocol):
    def add(
        self, sensor_id: str, reading_id: int, value: float,
        threshold_breached: str, message: str,
    ) -> AlertModel: ...
    def list_for_sensor(
            self, sensor_id: str, limit: int = 50, offset: int = 0) -> list[
                AlertModel]: ...


class SqlAlchemyAlertRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(
        self, sensor_id: str, reading_id: int, value: float,
        threshold_breached: str, message: str,
    ) -> AlertModel:
        alert = AlertModel(
            sensor_id=sensor_id, reading_id=reading_id, value=value,
            threshold_breached=threshold_breached, message=message,
        )
        self._session.add(alert)
        try:
            self._session.commit()
        except IntegrityError as exc:
            self._session.rollback()
            raise AlertCreationError(
                f"No se pudo crear la alerta: sensor_id '{sensor_id}' o "
                f"reading_id '{reading_id}' invalido"
            ) from exc
        self._session.refresh(alert)
        return alert

    def list_for_sensor(
            self, sensor_id: str, limit: int = 50, offset: int = 0) -> list[AlertModel]:
        stmt = (
            select(AlertModel)
            .where(AlertModel.sensor_id == sensor_id)
            .order_by(AlertModel.created_at.desc(), AlertModel.id.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(self._session.scalars(stmt).all())