""" exceptions.py
    Dia 5
    Codigo para definir las excepciones personalizadas
"""

#  Excepciones personalizadas para el manejo de errores en la API
class ReadingNotFoundError(Exception):
    """La lectura solicitada no existe."""


class SensorMismatchError(Exception):
    """El sensor_id de la ruta no coincide con el del cuerpo."""


class InvalidDateRangeError(Exception):
    """'from' es posterior a 'to'."""


class SensorNotFoundError(Exception):
    """El sensor solicitado no existe."""


class SensorAlreadyExistsError(Exception):
    """Ya existe un sensor con ese sensor_id."""