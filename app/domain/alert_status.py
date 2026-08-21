"""domain/alert_status.py
Logica pura: ciclo de vida de una alerta (maquina de estados simple).
"""
from enum import Enum


class AlertStatus(str, Enum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


class InvalidTransitionError(Exception):
    """La transicion de estado solicitada no es valida."""


_VALID_TRANSITIONS: dict[AlertStatus, set[AlertStatus]] = {
    AlertStatus.OPEN: {AlertStatus.ACKNOWLEDGED, AlertStatus.RESOLVED},
    AlertStatus.ACKNOWLEDGED: {AlertStatus.RESOLVED},
    AlertStatus.RESOLVED: set(),
}


def can_transition(current: AlertStatus, target: AlertStatus) -> bool:
    return target in _VALID_TRANSITIONS.get(current, set())