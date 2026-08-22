"""routers/readings.py
Dia 5 arreglo - POST ya no compara sensor_id de ruta vs body"""

# Importaciones
from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, status

from app.dependencies import (
    AnomalyDetectionServiceDep,
    ReadingServiceDep,
    SensorServiceDep,
)
from app.domain.reading_statistics import ReadingStatistics
from app.models.reading import ReadingModel
from app.schemas.reading import (
    ReadingStatsOut,
    SensorReadingIn,
    SensorReadingOut,
    SensorReadingUpdate,
)
from app.services.exceptions import (
    InvalidDateRangeError,
    ReadingNotFoundError,
    SensorNotFoundError,
)

router = APIRouter(tags=["readings"])


# GET /sensors/{id}/readings?limit=&offset=&from=&to=  -> 200
@router.get("/sensors/{sensor_id}/readings", response_model=list[SensorReadingOut])
def list_readings(
    sensor_id: str,
    service: ReadingServiceDep,
    sensor_service: SensorServiceDep,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    from_: datetime | None = Query(None, alias="from"),  # noqa: B008
    to: datetime | None = Query(None),  # noqa: B008
) -> list[ReadingModel]:
    try:
        sensor_service.get(sensor_id)  # 404 si el sensor no existe
        return service.history(
            sensor_id, limit=limit, offset=offset, date_from=from_, date_to=to
        )
    except SensorNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    except InvalidDateRangeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


# POST /sensors/{id}/readings  -> 201
@router.post(
    "/sensors/{sensor_id}/readings",
    response_model=SensorReadingOut,
    status_code=status.HTTP_201_CREATED,
)
def create_reading(
    sensor_id: str,
    reading: SensorReadingIn,
    service: ReadingServiceDep,
    sensor_service: SensorServiceDep,
    anomaly_service: AnomalyDetectionServiceDep,
) -> ReadingModel:
    try:
        sensor_service.get(sensor_id)
        new_reading = service.record_for_sensor(sensor_id, reading.value, reading.unit)
        anomaly_service.evaluate(sensor_id, new_reading.id, new_reading.value)
        return new_reading
    except SensorNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


# GET /readings/{id}  -> 200
@router.get("/readings/{reading_id}", response_model=SensorReadingOut)
def get_reading(reading_id: int, service: ReadingServiceDep) -> ReadingModel:
    try:
        return service.get(reading_id)
    except ReadingNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


# PATCH /readings/{id}  -> 200
@router.patch("/readings/{reading_id}", response_model=SensorReadingOut)
def update_reading(
    reading_id: int, patch: SensorReadingUpdate, service: ReadingServiceDep
) -> ReadingModel:
    try:
        return service.update_partial(reading_id, value=patch.value, unit=patch.unit)
    except ReadingNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


# DELETE /readings/{id}  -> 204 (desactivar, no borrar)
@router.delete("/readings/{reading_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reading(reading_id: int, service: ReadingServiceDep) -> None:
    try:
        service.deactivate(reading_id)
    except ReadingNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.get("/sensors/{sensor_id}/readings/stats", response_model=ReadingStatsOut)
def get_reading_stats(
    sensor_id: str,
    service: ReadingServiceDep,
    sensor_service: SensorServiceDep,
    from_: datetime | None = Query(None, alias="from"),  # noqa: B008
    to: datetime | None = Query(None),  # noqa: B008
) -> ReadingStatistics:
    try:
        sensor_service.get(sensor_id)
        return service.get_statistics(sensor_id, from_, to)
    except SensorNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
