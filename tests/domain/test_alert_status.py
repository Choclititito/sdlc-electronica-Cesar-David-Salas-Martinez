"""tests/domain/test_alert_status.py
Test en verde con la logica de dominio de alert_status.py.
"""
import pytest
from app.domain.alert_status import AlertStatus, can_transition, InvalidTransitionError


def test_open_to_acknowledged_is_valid():
    assert can_transition(AlertStatus.OPEN, AlertStatus.ACKNOWLEDGED) is True


def test_acknowledged_to_resolved_is_valid():
    assert can_transition(AlertStatus.ACKNOWLEDGED, AlertStatus.RESOLVED) is True


def test_open_to_resolved_directly_is_valid():
    # se permite resolver directo sin pasar por acknowledged
    assert can_transition(AlertStatus.OPEN, AlertStatus.RESOLVED) is True


def test_resolved_to_open_is_invalid():
    assert can_transition(AlertStatus.RESOLVED, AlertStatus.OPEN) is False


def test_resolved_to_acknowledged_is_invalid():
    assert can_transition(AlertStatus.RESOLVED, AlertStatus.ACKNOWLEDGED) is False


def test_same_status_transition_is_invalid():
    assert can_transition(AlertStatus.OPEN, AlertStatus.OPEN) is False