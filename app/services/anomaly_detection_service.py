"""services/anomaly_detection_service.py"""

from typing import Protocol

from app.domain.alert_severity import determine_severity
from app.models.sensor import SensorModel
from app.repositories.alert_repository import AlertRepository
from app.services.notifiers import AlertNotifier


class SensorThresholdLookup(Protocol):
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
            return

        severity = determine_severity(value, sensor.min_threshold, sensor.max_threshold)
        if severity is None:
            return

        breached = (
            "max"
            if sensor.max_threshold is not None and value > sensor.max_threshold
            else "min"
        )
        message = (
            f"[{severity.value.upper()}] "
            f"Valor {value} {breached} threshold para sensor {sensor_id}"
        )
        alert = self._alert_repo.add(
            sensor_id, reading_id, value, breached, severity.value, message
        )
        self._notifier.notify(alert)
