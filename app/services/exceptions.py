""" reading_service.py
    Dia 4        """

#Casos de excepcion para el servicio de lectura
class ReadingNotFoundError(Exception):
    """La lectura solicitada no existe."""

class SensorMismatchError(Exception):
    """El sensor_id de la ruta no coincide con el del cuerpo."""

class InvalidDateRangeError(Exception):
    """'from' es posterior a 'to'."""