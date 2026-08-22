"""services/alert_query_service.py"""

from app.domain.alert_status import AlertStatus, InvalidTransitionError, can_transition
from app.models.alert import AlertModel
from app.repositories.alert_repository import AlertRepository


class AlertNotFoundError(Exception):
    """La alerta solicitada no existe."""


class AlertQueryService:
    def __init__(self, repo: AlertRepository) -> None:
        self._repo = repo

    def list_for_sensor(
        self,
        sensor_id: str,
        limit: int = 50,
        offset: int = 0,
        status: str | None = None,
    ) -> list[AlertModel]:
        return self._repo.list_for_sensor(
            sensor_id, limit=limit, offset=offset, status=status
        )

    def change_status(self, alert_id: int, new_status: AlertStatus) -> AlertModel:
        alert = self._repo.get_by_id(alert_id)
        if alert is None:
            raise AlertNotFoundError(f"Alerta {alert_id} no encontrada")

        current = AlertStatus(alert.status)
        if not can_transition(current, new_status):
            raise InvalidTransitionError(
                f"No se puede pasar de '{current.value}' a '{new_status.value}'"
            )

        updated = self._repo.update_status(alert_id, new_status.value)
        assert updated is not None
        return updated
