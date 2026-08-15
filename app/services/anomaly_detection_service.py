"""services/anomaly_detection_service.py"""

from typing import Protocol

from app.models.sensor import SensorModel
from app.repositories.alert_repository import AlertRepository
from app.services.notifiers import AlertNotifier


class SensorThresholdLookup(Protocol):
    """Abstraccion minima: solo necesitamos poder buscar un sensor por id.
    Esto permite inyectar SensorRepository real o un fake en tests, sin que
    AnomalyDetectionService dependa de todo SensorService."""

    def get_by_sensor_id(self, sensor_id: str) -> SensorModel | None: ...


class AnomalyDetectionService:
    def __init__(
        self,
        alert_repo: AlertRepository,
        notifier: AlertNotifier,
        sensor_lookup: SensorThresholdLookup,
    ) -> None:
        self._alert_repo = alert_repo
        self._notifier = notifier
        self._sensor_lookup = sensor_lookup

    def evaluate(self, sensor_id: str, reading_id: int, value: float) -> None:
        sensor = self._sensor_lookup.get_by_sensor_id(sensor_id)
        if sensor is None:
            return  # sensor desconocido: no rompe el flujo de creacion de reading

        breached: str | None = None
        if sensor.min_threshold is not None and value < sensor.min_threshold:
            breached = "min"
        elif sensor.max_threshold is not None and value > sensor.max_threshold:
            breached = "max"

        if breached is None:
            return

        message = f"Valor {value} {breached} threshold para sensor {sensor_id}"
        alert = self._alert_repo.add(sensor_id, reading_id, value, breached, message)
        self._notifier.notify(alert)
