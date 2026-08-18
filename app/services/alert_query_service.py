"""services/alert_query_service.py
Capa de servicio para consulta de alertas, siguiendo el mismo patron que
SensorService y ReadingService (router -> service -> repository)."""

from app.models.alert import AlertModel
from app.repositories.alert_repository import AlertRepository


class AlertQueryService:
    def __init__(self, repo: AlertRepository) -> None:
        self._repo = repo

    def list_for_sensor(
        self, sensor_id: str, limit: int = 50, offset: int = 0
    ) -> list[AlertModel]:
        return self._repo.list_for_sensor(sensor_id, limit=limit, offset=offset)
