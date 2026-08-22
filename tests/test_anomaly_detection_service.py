"""tests/test_anomaly_detection_service.py"""

from dataclasses import dataclass, field

import pytest
from app.models.alert import AlertModel
from app.models.sensor import SensorModel


@dataclass
class FakeAlertRepository:
    _alerts: list[AlertModel] = field(default_factory=list)
    _next_id: int = 1

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
            id=self._next_id,
            sensor_id=sensor_id,
            reading_id=reading_id,
            value=value,
            threshold_breached=threshold_breached,
            severity=severity,
            message=message,
        )
        self._alerts.append(alert)
        self._next_id += 1
        return alert

    def list_for_sensor(self, sensor_id: str) -> list[AlertModel]:
        return [a for a in self._alerts if a.sensor_id == sensor_id]


@dataclass
class FakeAlertNotifier:
    """Notifier de prueba: solo registra que fue llamado, no notifica de verdad."""

    notified: list[AlertModel] = field(default_factory=list)

    def notify(self, alert: AlertModel) -> None:
        self.notified.append(alert)


@dataclass
class FakeSensorLookup:
    """Simula la consulta de thresholds de un sensor,
    sin tocar SensorRepository real."""

    sensors: dict[str, SensorModel] = field(default_factory=dict)

    def get_by_sensor_id(self, sensor_id: str) -> SensorModel | None:
        return self.sensors.get(sensor_id)


@pytest.fixture
def alert_repo() -> FakeAlertRepository:
    return FakeAlertRepository()


@pytest.fixture
def notifier() -> FakeAlertNotifier:
    return FakeAlertNotifier()


@pytest.fixture
def sensor_lookup() -> FakeSensorLookup:
    lookup = FakeSensorLookup()
    lookup.sensors["TEMP-01"] = SensorModel(
        id=1,
        sensor_id="TEMP-01",
        sensor_type="temperature",
        unit="C",
        min_threshold=-10.0,
        max_threshold=40.0,
    )
    lookup.sensors["HUM-01"] = SensorModel(
        id=2,
        sensor_id="HUM-01",
        sensor_type="humidity",
        unit="%",
        min_threshold=None,
        max_threshold=None,  # sin umbrales configurados
    )
    return lookup


@pytest.fixture
def service(alert_repo, notifier, sensor_lookup):
    from app.services.anomaly_detection_service import AnomalyDetectionService

    return AnomalyDetectionService(
        alert_repo=alert_repo, notifier=notifier, sensor_lookup=sensor_lookup
    )


def test_value_within_range_does_not_create_alert(service, alert_repo, notifier):
    service.evaluate(sensor_id="TEMP-01", reading_id=1, value=25.0)
    assert alert_repo.list_for_sensor("TEMP-01") == []
    assert notifier.notified == []


def test_value_above_max_threshold_creates_alert(service, alert_repo, notifier):
    service.evaluate(sensor_id="TEMP-01", reading_id=1, value=45.0)
    alerts = alert_repo.list_for_sensor("TEMP-01")
    assert len(alerts) == 1
    assert alerts[0].threshold_breached == "max"
    assert alerts[0].value == 45.0


def test_value_below_min_threshold_creates_alert(service, alert_repo, notifier):
    service.evaluate(sensor_id="TEMP-01", reading_id=1, value=-15.0)
    alerts = alert_repo.list_for_sensor("TEMP-01")
    assert len(alerts) == 1
    assert alerts[0].threshold_breached == "min"


def test_alert_notifies_via_injected_notifier(service, notifier):
    service.evaluate(sensor_id="TEMP-01", reading_id=1, value=45.0)
    assert len(notifier.notified) == 1
    assert notifier.notified[0].sensor_id == "TEMP-01"


def test_sensor_without_thresholds_never_creates_alert(service, alert_repo, notifier):
    """HUM-01 no tiene min/max_threshold configurados: cualquier valor es 'ok'."""
    service.evaluate(sensor_id="HUM-01", reading_id=2, value=999.0)
    assert alert_repo.list_for_sensor("HUM-01") == []
    assert notifier.notified == []


def test_unknown_sensor_does_not_raise_and_creates_no_alert(
    service, alert_repo, notifier
):
    """Sensor no encontrado en el lookup:
    se ignora silenciosamente, no rompe el flujo de creacion de reading."""
    service.evaluate(sensor_id="GHOST-99", reading_id=3, value=999.0)
    assert alert_repo.list_for_sensor("GHOST-99") == []
    assert notifier.notified == []
