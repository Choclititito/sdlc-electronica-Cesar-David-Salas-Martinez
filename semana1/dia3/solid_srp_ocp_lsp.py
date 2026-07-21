# S - Una clase, una responsabilidad: SensorReader lee; DataLogger persiste.
# O - AlertStrategy (ABC) con ConsoleAlert y FileAlert: agregar EmailAlert
#     manana NO toca el codigo existente.
# L - TemperatureSensor y HumiditySensor son intercambiables donde se espera
#     BaseSensor: process_sensor(sensor: BaseSensor) funciona con cualquiera.
"""
class AlertStrategy(ABC):
    @abstractmethod
    def send(self, message: str) -> None: ...
 
class AnomalyDetector:
    def __init__(self, alert: AlertStrategy, threshold: float) -> None:
        self._alert = alert
        self._threshold = threshold
 
    def check(self, reading: SensorReading) -> None:
        if reading.value > self._threshold:
            self._alert.send(f"Anomalia en {reading.sensor_id}")
"""
"""---------------------------------------------------------------------------------------------------------------"""
"""EJEMPLOS PROPIOS"""

"""S: Single Responsibility Principle"""

#Ejemplo correcto: Cada clase solo tiene una accion especifica que debe de hacer

class SensorReader:
    def read_data(self) -> float:
        return 25.5 #Regresa un valor para simular una lectura

class DatabaseLogger:
    def save(self, data: float) -> str:
        return f"Guardando {data} en BD..." #Regresa un mensaje para confirmar

class EmailAlerter:
    def send_alert(self) -> str:
        return "Enviando correo de alerta..." #regresa un mensaje para confirmar

#Ejemplo incorrecto: Se usa una sola clase para varios puntos diferentes

class SmartSensor:
    def __init__(self, sensor_id: str):
        self.sensor_id = sensor_id

    def read_data(self) -> float:
        # Lógica para leer hardware
        return 25.5

    def save_to_database(self, data: float):
        # Lógica para conectar a SQL y guardar
        print(f"Guardando {data} en BD...")

    def send_email_alert(self):
        # Lógica para conectarse a un servidor SMTP
        print("Enviando correo de alerta...")

"""O: Open-Closed Principle"""

#Ejemplo correcto: Es facil el poder agregar alguna otra funcion parecida, sin modificar el codigo base
from abc import ABC, abstractmethod

class AlertStrategy(ABC): #Se usa el ejemplo proporcionado
    @abstractmethod
    def send(self, message: str) -> None:
        pass

class ConsoleAlert(AlertStrategy): #Se ejemplifica como seria el agregado de estas funcionas que menciona el ejemplo
    def send(self, message: str) -> None:
        print(f"Consola: {message}")

class EmailAlert(AlertStrategy):
    def send(self, message: str) -> None:
        print(f"Email: {message}")


#Ejemplo incorrecto: Se debe de modificar el codigo base para agregar funciones nuevas
class AlertSystem:
    def send_alert(self, alert_type: str, message: str):
        if alert_type == "console":
            print(f"Consola: {message}")
        elif alert_type == "email":
            print(f"Enviando Email: {message}")
#El codigo se seguiria alargando si se quieren agregar mas funciones

"""L: Liskov Substitution Principle"""
#Ejemplo correcto
class BaseSensor:
    def get_reading(self) -> float:
        return 0.0

class TemperatureSensor(BaseSensor):
    def get_reading(self) -> float:
        return 25.5  # Respeta el retorno float

class HumiditySensor(BaseSensor):
    def get_reading(self) -> float:
        return 60.2  # Respeta el retorno float

def print_sensor_data(sensor: BaseSensor):
    # Funciona perfectamente sin importar si le pasas Temperatura o Humedad
    print(f"Lectura: {sensor.get_reading()}")

#Ejemplo incorrecto
class BaseSensor:
    def get_reading(self) -> float:
        return 0.0

class TemperatureSensormal(BaseSensor):
    def get_reading(self) -> str:
        # Rompe Liskov: devuelve un string en lugar de un float
        return "25 grados" 

class DummySensor(BaseSensor):
    def get_reading(self) -> float:
        # Rompe Liskov: la función explota en lugar de dar una lectura
        raise NotImplementedError("Este sensor no lee nada")