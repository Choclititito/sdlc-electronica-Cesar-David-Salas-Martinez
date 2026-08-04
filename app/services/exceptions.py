""" services/exceptions.py
    Dia 5 arreglo - se elimina SensorMismatchError"""

# Vocabulario de errores de dominio: no saben nada de HTTP, el router los traduce

class ReadingNotFoundError(Exception):
    """La lectura solicitada no existe."""


class InvalidDateRangeError(Exception):
    """'from' es posterior a 'to'."""


class SensorNotFoundError(Exception):
    """El sensor solicitado no existe."""


class SensorAlreadyExistsError(Exception):
    """Ya existe un sensor con ese sensor_id."""