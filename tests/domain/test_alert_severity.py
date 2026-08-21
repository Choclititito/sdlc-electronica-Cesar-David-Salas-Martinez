"""tests/domain/test_alert_severity.py
TDD: este test se escribe ANTES de que exista app.domain.alert_severity.
Debe fallar con ImportError al principio.
"""
import pytest
from app.domain.alert_severity import determine_severity, AlertSeverity


def test_value_within_range_returns_none():
    # 25 esta dentro de [-10, 40]: no hay severidad, no hay alerta
    assert determine_severity(value=25.0, min_threshold=-10.0, max_threshold=40.0) is None


def test_value_slightly_above_max_is_warning():
    # 42 supera el max (40) por 2, menos del 20% del rango de referencia
    assert determine_severity(value=42.0, min_threshold=-10.0, max_threshold=40.0) == AlertSeverity.WARNING


def test_value_far_above_max_is_critical():
    # 80 supera el max (40) por mucho
    assert determine_severity(value=80.0, min_threshold=-10.0, max_threshold=40.0) == AlertSeverity.CRITICAL


def test_value_slightly_below_min_is_warning():
    assert determine_severity(value=-12.0, min_threshold=-10.0, max_threshold=40.0) == AlertSeverity.WARNING


def test_value_far_below_min_is_critical():
    assert determine_severity(value=-50.0, min_threshold=-10.0, max_threshold=40.0) == AlertSeverity.CRITICAL


def test_no_thresholds_configured_returns_none():
    assert determine_severity(value=999.0, min_threshold=None, max_threshold=None) is None


def test_value_exactly_at_max_threshold_is_not_alert():
    # limite inclusivo: exactamente en el borde no es anomalia
    assert determine_severity(value=40.0, min_threshold=-10.0, max_threshold=40.0) is None