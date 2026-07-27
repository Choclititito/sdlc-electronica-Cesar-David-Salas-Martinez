"""AlertManager: envío de alertas ante anomalías detectadas (HU-04).

Usa el patrón Strategy: AlertStrategy es abstracta y define el contrato
send(event); ConsoleAlertStrategy y FileAlertStrategy son implementaciones
concretas. AlertManager orquesta N estrategias inyectadas y aplica la
deduplicación de alertas activas por (sensor_id, tipo)."""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from anomaly_detector import AnomalyEvent, AnomalyType


class AlertStrategy(ABC): # Contrato abstracto para cualquier canal de notificación
    """Contrato abstracto para cualquier canal de notificación de alertas."""

    @abstractmethod
    def send(self, event: AnomalyEvent) -> None:
        raise NotImplementedError


class ConsoleAlertStrategy(AlertStrategy): # Aviso de alerta por consola
    """Envía la alerta a la salida estándar (stdout)."""

    def send(self, event: AnomalyEvent) -> None:
        print(self._format(event))

    @staticmethod
    def _format(event: AnomalyEvent) -> str:
        return (
            f"[ALERTA] sensor={event.sensor_id} tipo={event.anomaly_type.value} "
            f"valor={event.value} umbral={event.threshold} hora={event.timestamp.isoformat()}"
        )


class FileAlertStrategy(AlertStrategy): # Escribe alertas en un archivo de log
    """Escribe cada alerta como una línea nueva en un archivo de log (append)."""

    def __init__(self, filepath: str):
        self.filepath = filepath

    def send(self, event: AnomalyEvent) -> None:
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(self._format(event) + "\n")

    @staticmethod
    def _format(event: AnomalyEvent) -> str:
        return (
            f"{event.timestamp.isoformat()} sensor={event.sensor_id} "
            f"tipo={event.anomaly_type.value} valor={event.value} umbral={event.threshold}"
        )


class AlertManager: 
    """Orquesta el envío de una anomalía a todas las estrategias registradas,
    evitando reenviar la misma alerta mientras la anomalía siga activa (HU-04)."""

    def __init__(self, strategies: List[AlertStrategy]):
        self.strategies = strategies
        self._active_alerts: Dict[Tuple[str, AnomalyType], bool] = {}

    def notify(self, event: AnomalyEvent) -> None:
        key = (event.sensor_id, event.anomaly_type)
        if self._active_alerts.get(key, False):
            return  # ya existe una alerta activa para esta anomalía: no duplicar

        self._active_alerts[key] = True
        for strategy in self.strategies:
            strategy.send(event)

    def resolve(self, sensor_id: str, anomaly_type: AnomalyType) -> None:
        """Marca la anomalía como resuelta, permitiendo que una futura
        reaparición vuelva a generar una alerta."""
        self._active_alerts[(sensor_id, anomaly_type)] = False
