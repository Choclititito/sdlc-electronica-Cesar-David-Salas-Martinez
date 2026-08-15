"""services/notifiers.py
Estrategias de notificacion de alertas."""

import logging
from typing import Protocol

from app.models.alert import AlertModel

logger = logging.getLogger(__name__)


class AlertNotifier(Protocol):
    def notify(self, alert: AlertModel) -> None: ...


class LogAlertNotifier:
    """Estrategia por defecto: escribe la alerta al log del servidor."""

    def notify(self, alert: AlertModel) -> None:
        logger.warning(
            "ALERTA sensor=%s valor=%s umbral=%s: %s",
            alert.sensor_id,
            alert.value,
            alert.threshold_breached,
            alert.message,
        )


class NoOpAlertNotifier:
    """Estrategia nula: no hace nada. Util para tests o entornos donde no
    se quiere notificar activamente."""

    def notify(self, alert: AlertModel) -> None:
        pass
