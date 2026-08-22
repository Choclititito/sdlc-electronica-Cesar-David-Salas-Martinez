"""repositories/alert_repository.py"""

from typing import Protocol

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.alert import AlertModel
from app.services.exceptions import AlertCreationError


class AlertRepository(Protocol):
    def add(
        self,
        sensor_id: str,
        reading_id: int,
        value: float,
        threshold_breached: str,
        severity: str,
        message: str,
    ) -> AlertModel: ...
    def list_for_sensor(
        self,
        sensor_id: str,
        limit: int = 50,
        offset: int = 0,
        status: str | None = None,
    ) -> list[AlertModel]: ...
    def get_by_id(self, alert_id: int) -> AlertModel | None: ...
    def update_status(self, alert_id: int, new_status: str) -> AlertModel | None: ...
    def count_open(self) -> int: ...


class SqlAlchemyAlertRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(
        self,
        sensor_id: str,
        reading_id: int,
        value: float,
        threshold_breached: str,
        severity: str,
        message: str,
    ) -> AlertModel:
        alert = AlertModel(
            sensor_id=sensor_id,
            reading_id=reading_id,
            value=value,
            threshold_breached=threshold_breached,
            severity=severity,
            message=message,
        )
        self._session.add(alert)
        try:
            self._session.commit()
        except IntegrityError as exc:
            self._session.rollback()
            raise AlertCreationError(
                f"No se pudo crear la alerta: sensor_id "
                f"'{sensor_id}' o reading_id '{reading_id}' invalido"
            ) from exc
        self._session.refresh(alert)
        return alert

    def list_for_sensor(
        self,
        sensor_id: str,
        limit: int = 50,
        offset: int = 0,
        status: str | None = None,
    ) -> list[AlertModel]:
        stmt = select(AlertModel).where(AlertModel.sensor_id == sensor_id)
        if status is not None:
            stmt = stmt.where(AlertModel.status == status)
        stmt = (
            stmt.order_by(AlertModel.created_at.desc(), AlertModel.id.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(self._session.scalars(stmt).all())

    def get_by_id(self, alert_id: int) -> AlertModel | None:
        return self._session.get(AlertModel, alert_id)

    def update_status(self, alert_id: int, new_status: str) -> AlertModel | None:
        alert = self.get_by_id(alert_id)
        if alert is None:
            return None
        alert.status = new_status
        self._session.commit()
        self._session.refresh(alert)
        return alert
    
    def count_open(self) -> int:
        stmt = select(func.count()).select_from(AlertModel).where(
            AlertModel.status == "open")
        return self._session.scalar(stmt) or 0
