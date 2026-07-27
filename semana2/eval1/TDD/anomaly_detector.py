"""AnomalyDetector: detecta anomalías de temperatura/humedad (HU-02, HU-03).

Los umbrales se inyectan por constructor -- NUNCA hardcodeados en el cuerpo
de la clase -- para que sean configurables sin tocar el código (requisito
que originalmente cubría HU-07, hoy eliminada del backlog, pero cuyo
principio de diseño se conserva aquí)."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Tuple

from sensor_reading import SensorReading


class AnomalyType(Enum): # Tipos de anomalías reconocidos
    HIGH_TEMPERATURE = "temperatura_alta"
    HIGH_HUMIDITY = "humedad_alta"


@dataclass(frozen=True) #datos sobre la anomalia detectada, para su notificacion
class AnomalyEvent:
    sensor_id: str
    anomaly_type: AnomalyType
    value: float
    threshold: float
    timestamp: datetime


class AnomalyDetector: # Donde se detectan las anomalias 
    def __init__(self, temperature_threshold: float, humidity_threshold: float):
        """Los umbrales son OBLIGATORIOS y se inyectan en tiempo de construcción.
        No existen valores por defecto para evitar umbrales implícitos/hardcodeados."""
        if temperature_threshold is None or humidity_threshold is None:
            raise ValueError("Los umbrales deben inyectarse explícitamente")
        self.temperature_threshold = temperature_threshold
        self.humidity_threshold = humidity_threshold
        # Estado de anomalías activas por (sensor_id, tipo) -> bool
        self._active_anomalies: Dict[Tuple[str, AnomalyType], bool] = {}

    def has_active_anomaly(self, sensor_id: str, anomaly_type: AnomalyType) -> bool: 
        # Se ve si la anomalia sigue activa
        return self._active_anomalies.get((sensor_id, anomaly_type), False)

    def evaluate(self, reading: SensorReading) -> List[AnomalyEvent]:
        """Evalúa una lectura contra los umbrales inyectados.
        Devuelve la lista de NUEVOS eventos de anomalía abiertos en esta lectura
        (una anomalía que se cierra no genera un evento en la lista de retorno,
        solo actualiza el estado interno, según HU-02)."""
        if not reading.is_valid():
            return []

        new_events: List[AnomalyEvent] = []

        new_events += self._check_dimension(
            reading, AnomalyType.HIGH_TEMPERATURE, reading.temperature, self.temperature_threshold
        )
        new_events += self._check_dimension(
            reading, AnomalyType.HIGH_HUMIDITY, reading.humidity, self.humidity_threshold
        )

        return new_events

    def _check_dimension( 
        self, reading: SensorReading, anomaly_type: AnomalyType, value: float, threshold: float
    ) -> List[AnomalyEvent]: # este def funciona para cada dimension (temp y humedad)
        key = (reading.sensor_id, anomaly_type)
        is_anomalous = value > threshold  # estrictamente mayor, según criterio de aceptación
        was_active = self._active_anomalies.get(key, False)

        if is_anomalous and not was_active:
            self._active_anomalies[key] = True
            return [AnomalyEvent(
                sensor_id=reading.sensor_id,
                anomaly_type=anomaly_type,
                value=value,
                threshold=threshold,
                timestamp=reading.timestamp,
            )]

        if not is_anomalous and was_active:
            self._active_anomalies[key] = False
            return []

        # Sigue anómalo (ya activo) o sigue normal: sin evento nuevo
        return []
