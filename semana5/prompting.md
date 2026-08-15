# PROMPTS UTILIZADOS

## Ejemplo

```
CONTEXTO:
API FastAPI (Python 3.12) para gestion de sensores.
SQLAlchemy 2.x tipado, arquitectura en capas.

TAREA:
escribe una funcion pura celsius_to_fahrenheit(c: float) -> float en semana5/conversions.py.

RESTRICCIONES: type hints completos, docstring, sin dependencias externas, redondeo a 2 decimales.

ENTREGA: solo la funcion, sin explicacion.
```

---

## 3 Prompts buenos junto a sus contrapartes

### 1.1. Malo

> "Haz un codigo para estadísticas agregadas por sensor"

**Resultado** (agregado en `reading_service.py`):

```python
def aggregate_for_sensor(
    self,
    sensor_id: str,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> dict[str, int | float | None]:
    """Devuelve estadísticas agregadas de las lecturas de un sensor.

    Estadísticas: `count`, `sum`, `min`, `max`, `mean`, `std`.
    Valores numéricos se redondean a 2 decimales; cuando no hay lecturas
    se devuelven `None` para `min`/`max`/`mean`/`std` y `0` para `count`/`sum`.
    """
    if date_from is not None and date_to is not None and date_from > date_to:
        raise InvalidDateRangeError("'from' no puede ser posterior a 'to'")

    readings = self._repo.list_for_sensor(
        sensor_id, limit=10_000_000, offset=0, date_from=date_from, date_to=date_to
    )
    values = [r.value for r in readings]
    count = len(values)
    if count == 0:
        return {
            "count": 0,
            "sum": 0.0,
            "min": None,
            "max": None,
            "mean": None,
            "std": None,
        }

    total = sum(values)
    mn = min(values)
    mx = max(values)
    m = mean(values)
    std = pstdev(values) if count > 0 else 0.0

    return {
        "count": count,
        "sum": round(total, 2),
        "min": round(mn, 2),
        "max": round(mx, 2),
        "mean": round(m, 2),
        "std": round(std, 2),
    }
```

### 1.2. Bueno

```
CONTEXTO:
API FastAPI (Python 3.12) para gestion de sensores.
SQLAlchemy 2.x tipado, arquitectura en capas.

TAREA:
escribe una funcion que me permitiera agregar estadísticas agregadas por sensor — un endpoint tipo
GET /sensors/{id}/readings/stats que devuelva mínimo, máximo, promedio de las lecturas en un rango
de fechas el codigo dejalo en un archivo en semana5/estadisticas.py.

RESTRICCIONES: type hints completos, respeta el patron Protocol existente, la agregacion debe
ejecutarse en la base de datos (no con Python sobre una lista), devuelve 404 si el sensor no existe,
devuelve valores null si no hay lecturas en el rango.

ENTREGA: solo la funcion, sin explicacion.
```

**Resultado** (en `estadisticas.py`):

```python
from datetime import datetime
from typing import Dict, Optional

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.reading import ReadingModel
from app.models.sensor import SensorModel


def aggregate_readings_stats(
    session: Session,
    sensor_id: str,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> Dict[str, Optional[float]]:
    """Return aggregated statistics (min, max, mean) for a sensor's readings.

    Raises HTTPException 404 if the sensor does not exist. Returns `None` for
    each statistic when there are no readings in the given range.
    """
    sensor_stmt = select(SensorModel).where(SensorModel.sensor_id == sensor_id)
    sensor = session.scalar(sensor_stmt)
    if sensor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor '{sensor_id}' no encontrado",
        )

    stmt = select(
        func.count(ReadingModel.id),
        func.min(ReadingModel.value),
        func.max(ReadingModel.value),
        func.avg(ReadingModel.value),
    ).where(
        ReadingModel.sensor_id == sensor_id,
        ReadingModel.is_active.is_(True),
    )
    if date_from is not None:
        stmt = stmt.where(ReadingModel.created_at >= date_from)
    if date_to is not None:
        stmt = stmt.where(ReadingModel.created_at <= date_to)

    result = session.execute(stmt).one()
    count, min_v, max_v, avg_v = result

    if count == 0 or (min_v is None and max_v is None and avg_v is None):
        return {"min": None, "max": None, "mean": None}

    return {
        "min": float(min_v) if min_v is not None else None,
        "max": float(max_v) if max_v is not None else None,
        "mean": float(avg_v) if avg_v is not None else None,
    }
```

---

### 2.1. Malo

> "Dame un codigo para tener umbrales de alerta por sensor"

**Resultado 1** (`threshold.py`):

```python
"""models/threshold.py
Umbrales configurables por sensor.
"""

from datetime import datetime, timezone

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class ThresholdModel(Base):
    __tablename__ = "thresholds"
    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[str] = mapped_column(
        ForeignKey("sensors.sensor_id", name="fk_thresholds_sensor_id"), index=True
    )
    min_value: Mapped[float | None]
    max_value: Mapped[float | None]
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    is_active: Mapped[bool] = mapped_column(default=True)
```

**Resultado 2** (`threshold_repository.py`):

```python
"""threshold_repository.py
Repositorio para umbrales por sensor.
"""

from typing import Protocol

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.threshold import ThresholdModel


class ThresholdRepository(Protocol):
    def add(
        self, sensor_id: str, min_value: float | None, max_value: float | None
    ) -> ThresholdModel: ...
    def get_by_sensor_id(self, sensor_id: str) -> ThresholdModel | None: ...
    def update(
        self, sensor_id: str, min_value: float | None, max_value: float | None
    ) -> ThresholdModel | None: ...
    def deactivate(self, sensor_id: str) -> ThresholdModel | None: ...


class SqlAlchemyThresholdRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(
        self, sensor_id: str, min_value: float | None, max_value: float | None
    ) -> ThresholdModel:
        t = ThresholdModel(
            sensor_id=sensor_id, min_value=min_value, max_value=max_value
        )
        self._session.add(t)
        self._session.commit()
        self._session.refresh(t)
        return t

    def get_by_sensor_id(self, sensor_id: str) -> ThresholdModel | None:
        stmt = select(ThresholdModel).where(
            ThresholdModel.sensor_id == sensor_id, ThresholdModel.is_active.is_(True)
        )
        return self._session.scalar(stmt)

    def update(
        self, sensor_id: str, min_value: float | None, max_value: float | None
    ) -> ThresholdModel | None:
        t = self.get_by_sensor_id(sensor_id)
        if t is None:
            return None
        t.min_value = min_value
        t.max_value = max_value
        self._session.commit()
        self._session.refresh(t)
        return t

    def deactivate(self, sensor_id: str) -> ThresholdModel | None:
        t = self.get_by_sensor_id(sensor_id)
        if t is None:
            return None
        t.is_active = False
        self._session.commit()
        self._session.refresh(t)
        return t
```

**Resultado 3** (`threshold_service.py`):

```python
"""threshold_service.py
Lógica de negocio para umbrales por sensor.
"""

from typing import TypedDict

from app.repositories.threshold_repository import ThresholdRepository
from app.services.sensor_service import SensorService
from app.models.threshold import ThresholdModel
from app.services.exceptions import SensorNotFoundError


class ThresholdInfo(TypedDict):
    sensor_id: str
    min_value: float | None
    max_value: float | None


class ThresholdService:
    def __init__(
        self, repo: ThresholdRepository, sensor_service: SensorService
    ) -> None:
        self._repo = repo
        self._sensor_service = sensor_service

    def set_threshold(
        self, sensor_id: str, min_value: float | None, max_value: float | None
    ) -> ThresholdModel:
        # Verificar existencia del sensor (lanza SensorNotFoundError si no existe)
        self._sensor_service.get(sensor_id)
        existing = self._repo.get_by_sensor_id(sensor_id)
        if existing is None:
            return self._repo.add(sensor_id, min_value, max_value)
        return self._repo.update(sensor_id, min_value, max_value)

    def get_threshold(self, sensor_id: str) -> ThresholdInfo | None:
        t = self._repo.get_by_sensor_id(sensor_id)
        if t is None:
            return None
        return {
            "sensor_id": t.sensor_id,
            "min_value": t.min_value,
            "max_value": t.max_value,
        }

    def remove_threshold(self, sensor_id: str) -> None:
        self._repo.deactivate(sensor_id)

    def check_value(self, sensor_id: str, value: float) -> dict:
        """Devuelve dict con 'status' y detalles: 'ok', 'below_min', 'above_max'."""
        t = self._repo.get_by_sensor_id(sensor_id)
        if t is None:
            # Si no hay umbral configurado, se considera 'ok'
            return {"status": "ok", "reason": "no_threshold"}
        if t.min_value is not None and value < t.min_value:
            return {"status": "breach", "type": "below_min", "threshold": t.min_value}
        if t.max_value is not None and value > t.max_value:
            return {"status": "breach", "type": "above_max", "threshold": t.max_value}
        return {"status": "ok"}
```

### 2.2. Bueno

```
CONTEXTO:
API FastAPI (Python 3.12) para gestion de sensores.
SQLAlchemy 2.x tipado, arquitectura en capas.

TAREA:
Agrega dos columnas opcionales a SensorModel: min_threshold y max_threshold (float, nullable).
Al crear una Reading, si el sensor tiene thresholds definidos y el value cae fuera de ese rango,
el schema de salida SensorReadingOut debe incluir un campo is_alert: bool.
el codigo resultante ponlo en semana5/alertas_sensor.py.

RESTRICCIONES: los thresholds son opcionales, si un sensor no lo tiene no genera error, no reemplaza
la validacion de rango fisico que ya existe

ENTREGA: solo el codigo, sin explicacion.
```

**Resultado** (`alertas_sensor.py`):

```python
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.models.reading import ReadingModel
from app.models.sensor import SensorModel
from app.repositories.reading_repository import ReadingRepository
from app.repositories.sensor_repository import SensorRepository


class SensorReadingOutWithAlert(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    sensor_id: str
    value: float
    unit: str
    created_at: datetime
    is_active: bool
    is_alert: bool


def _sensor_thresholds(
    session: Session, sensor_id: str
) -> tuple[float | None, float | None]:
    sensor = (
        session.query(SensorModel).filter(SensorModel.sensor_id == sensor_id).first()
    )
    if sensor is None:
        return (None, None)
    # Support both explicit columns on SensorModel (`min_threshold`, `max_threshold`)
    # or absence of those attributes (return None).
    min_th = getattr(sensor, "min_threshold", None)
    max_th = getattr(sensor, "max_threshold", None)
    return (min_th, max_th)


def reading_to_out_with_alert(
    session: Session, reading: ReadingModel
) -> SensorReadingOutWithAlert:
    min_th, max_th = _sensor_thresholds(session, reading.sensor_id)
    is_alert = False
    if min_th is not None and reading.value < min_th:
        is_alert = True
    if max_th is not None and reading.value > max_th:
        is_alert = True
    # Build the output model using attributes from the ReadingModel
    return SensorReadingOutWithAlert(
        id=reading.id,
        sensor_id=reading.sensor_id,
        value=reading.value,
        unit=reading.unit,
        created_at=reading.created_at,
        is_active=reading.is_active,
        is_alert=is_alert,
    )


def create_reading_and_out_with_alert(
    session: Session,
    sensor_id: str,
    value: float,
    unit: str,
    reading_repo: ReadingRepository,
    sensor_repo: SensorRepository | None = None,
) -> SensorReadingOutWithAlert:
    # Persist the reading using the provided repository
    reading = reading_repo.add(sensor_id, value, unit)
    # Use the session to evaluate thresholds and return enriched output
    return reading_to_out_with_alert(session, reading)
```

---

### 3.1. Malo

> "hazme un codigo para exportar las lecturas a csv"

**Resultado** (`export_cvs.py`):

```python
from __future__ import annotations

from datetime import datetime
from typing import Optional
import csv
import io

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.reading import ReadingModel


def export_readings_to_csv(
    session: Session,
    file_path: str,
    sensor_id: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    include_header: bool = True,
) -> str:
    """Export readings to a CSV file and return the file path.

    Args:
        session: SQLAlchemy session to read readings.
        file_path: Destination filesystem path to write CSV.
        sensor_id: Optional sensor id to filter readings.
        date_from: Optional inclusive lower bound for `created_at`.
        date_to: Optional inclusive upper bound for `created_at`.
        include_header: Whether to write a header row.

    Returns:
        The `file_path` written.
    """
    stmt = select(ReadingModel).where(ReadingModel.is_active.is_(True))
    if sensor_id is not None:
        stmt = stmt.where(ReadingModel.sensor_id == sensor_id)
    if date_from is not None:
        stmt = stmt.where(ReadingModel.created_at >= date_from)
    if date_to is not None:
        stmt = stmt.where(ReadingModel.created_at <= date_to)

    readings = session.scalars(stmt).all()

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if include_header:
            writer.writerow(
                ["id", "sensor_id", "value", "unit", "created_at", "is_active"]
            )
        for r in readings:
            writer.writerow(
                [
                    r.id,
                    r.sensor_id,
                    r.value,
                    r.unit,
                    r.created_at.isoformat() if r.created_at is not None else "",
                    bool(r.is_active),
                ]
            )

    return file_path


def export_readings_to_csv_bytes(
    session: Session,
    sensor_id: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    include_header: bool = True,
) -> bytes:
    """Return CSV content (bytes) for the selected readings.

    Useful for returning a download response without writing to disk.
    """
    stmt = select(ReadingModel).where(ReadingModel.is_active.is_(True))
    if sensor_id is not None:
        stmt = stmt.where(ReadingModel.sensor_id == sensor_id)
    if date_from is not None:
        stmt = stmt.where(ReadingModel.created_at >= date_from)
    if date_to is not None:
        stmt = stmt.where(ReadingModel.created_at <= date_to)

    readings = session.scalars(stmt).all()

    buf = io.StringIO()
    writer = csv.writer(buf)
    if include_header:
        writer.writerow(["id", "sensor_id", "value", "unit", "created_at", "is_active"])
    for r in readings:
        writer.writerow(
            [
                r.id,
                r.sensor_id,
                r.value,
                r.unit,
                r.created_at.isoformat() if r.created_at is not None else "",
                bool(r.is_active),
            ]
        )

    return buf.getvalue().encode("utf-8")
```

### 3.2. Bueno

```
CONTEXTO:
API FastAPI (Python 3.12) para gestion de sensores.
SQLAlchemy 2.x tipado, arquitectura en capas.

TAREA:
Agrega un endpoint GET /sensors/{sensor_id}/readings/export que devuelva un archivo CSV descargable
con las lecturas del sensor (columnas: id, value, unit, created_at), usando StreamingResponse
y el modulo csv de la libreria estandar. el codigo mandalo a un archivo en semana5/csv.py

RESTRICCIONES: no cargar todo en memoria si es evitable, incluir header
Content-Disposition: attachment; filename=readings_{sensor_id}.csv, reutiliza
ReadingService.history() existente (no dupliques la logica de consulta), 404 si el sensor no existe.

ENTREGA: solo la funcion, sin explicacion.
```

**Resultado**:

```python
from io import StringIO
import csv

from datetime import datetime
from typing import Generator

from fastapi import Depends, Query
from fastapi.responses import StreamingResponse

from app.dependencies import ReadingServiceDep, SensorServiceDep


def export_readings_csv(
    sensor_id: str,
    service: ReadingServiceDep,
    sensor_service: SensorServiceDep,
    from_: datetime | None = Query(None, alias="from"),
    to: datetime | None = Query(None),
    chunk_size: int = Query(500, ge=1, le=5000),
) -> StreamingResponse:
    # Ensure sensor exists (raises 404 via SensorService if missing)
    sensor_service.get(sensor_id)

    def row_generator() -> Generator[bytes, None, None]:
        # yield header
        buf = StringIO()
        writer = csv.writer(buf)
        writer.writerow(["id", "value", "unit", "created_at"])
        yield buf.getvalue().encode("utf-8")

        offset = 0
        while True:
            readings = service.history(
                sensor_id, limit=chunk_size, offset=offset, date_from=from_, date_to=to
            )
            if not readings:
                break
            for r in readings:
                buf = StringIO()
                writer = csv.writer(buf)
                writer.writerow(
                    [
                        r.id,
                        r.value,
                        r.unit,
                        r.created_at.isoformat()
                        if getattr(r, "created_at", None) is not None
                        else "",
                    ]
                )
                yield buf.getvalue().encode("utf-8")
            offset += len(readings)

    filename = f"readings_{sensor_id}.csv"
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return StreamingResponse(row_generator(), media_type="text/csv", headers=headers)
```

---

## Conclusiones

Podemos ver como con un mejor uso de los prompts, la inteligencia artificial nos puede dar mejores resultados. Los mayores cambios que considero es el poder tener puntos aclarados desde la parte donde estamos explicándole a la IA, y darle un contexto de en qué estamos trabajando le ayuda para saber qué cosas puede utilizar y cuáles no.

Aunque al usar la inteligencia artificial de Copilot, esta podía acceder a los archivos en los que estoy trabajando para poder armar su propio contexto, además noté cómo conforme la conversación avanzaba, empezaba a tomar cosas que le había pedido en los prompts buenos para hacer los siguientes códigos, así haciendo que los códigos con los prompts malos tuvieran más estructura, sin embargo les faltaban detalles, y podían diferir un poco de la visión original que tenía, ya que eran bastante ambiguos.

En conclusión, puedo decir que sí ayuda bastante darle instrucciones concretas a la IA para que esta pueda hacer mejor su trabajo.