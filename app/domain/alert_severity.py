"""domain/alert_severity.py
Logica pura: determina la severidad de una lectura respecto a los
thresholds de su sensor. Sin dependencias de FastAPI/SQLAlchemy.
"""

from enum import Enum

# Que tan lejos del threshold (como fraccion del rango) se considera CRITICAL
_CRITICAL_MARGIN_FRACTION = 0.5


class AlertSeverity(str, Enum):
    WARNING = "warning"
    CRITICAL = "critical"


def determine_severity(
    value: float, min_threshold: float | None, max_threshold: float | None
) -> AlertSeverity | None:
    """Determina la severidad de un valor respecto a sus umbrales.

    Retorna None si el valor esta dentro de rango o no hay umbrales
    configurados. El margen de referencia para CRITICAL se calcula sobre
    el ancho del rango [min_threshold, max_threshold] cuando ambos existen;
    si solo hay uno de los dos, se usa un margen absoluto fijo.
    """
    if min_threshold is None and max_threshold is None:
        return None

    range_width = None
    if min_threshold is not None and max_threshold is not None:
        range_width = max_threshold - min_threshold

    if max_threshold is not None and value > max_threshold:
        excess = value - max_threshold
        margin = (range_width * _CRITICAL_MARGIN_FRACTION) if range_width else 10.0
        return AlertSeverity.CRITICAL if excess > margin else AlertSeverity.WARNING

    if min_threshold is not None and value < min_threshold:
        deficit = min_threshold - value
        margin = (range_width * _CRITICAL_MARGIN_FRACTION) if range_width else 10.0
        return AlertSeverity.CRITICAL if deficit > margin else AlertSeverity.WARNING

    return None
