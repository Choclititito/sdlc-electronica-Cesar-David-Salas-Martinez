"""domain/reading_statistics.py
Logica pura: calcula estadisticas agregadas (min, max, promedio) sobre
una lista de valores. Sin dependencias de FastAPI/SQLAlchemy — la capa
de repositorio decide COMO obtener esos valores (idealmente con
agregacion en BD, no trayendo todas las filas).
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ReadingStatistics:
    count: int
    minimum: float | None
    maximum: float | None
    average: float | None


def compute_statistics(values: list[float]) -> ReadingStatistics:
    """Calcula min, max y promedio (redondeado a 2 decimales) de una
    lista de valores. Lista vacia devuelve todos los campos en None
    excepto count=0."""
    if not values:
        return ReadingStatistics(count=0, minimum=None, maximum=None, average=None)

    return ReadingStatistics(
        count=len(values),
        minimum=min(values),
        maximum=max(values),
        average=round(sum(values) / len(values), 2),
    )