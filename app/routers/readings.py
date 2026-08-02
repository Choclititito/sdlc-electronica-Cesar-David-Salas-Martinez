""" readings.py
    Dia 4          """

# Importaciones de los modulos necesarios
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query, status
from app.dependencies import ReadingServiceDep
from app.schemas.reading import SensorReadingIn, SensorReadingOut, SensorReadingUpdate
from app.services.exceptions import (
    ReadingNotFoundError, SensorMismatchError, InvalidDateRangeError,
)
# Definimos el router para las rutas relacionadas con las lecturas
router = APIRouter(tags=["readings"])


# GET /sensors/{id}/readings?limit=50&offset=0&from=...&to=...  -> 200
@router.get("/sensors/{sensor_id}/readings", response_model=list[SensorReadingOut])
def list_readings(
    sensor_id: str,
    service: ReadingServiceDep,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    from_: datetime | None = Query(None, alias="from"),
    to: datetime | None = Query(None),
):
    try:
        return service.history(sensor_id, limit=limit, offset=offset, date_from=from_, date_to=to)
    except InvalidDateRangeError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


# POST /sensors/{id}/readings  -> 201
@router.post(
    "/sensors/{sensor_id}/readings",
    response_model=SensorReadingOut,
    status_code=status.HTTP_201_CREATED,
)
def create_reading(sensor_id: str, reading: SensorReadingIn, service: ReadingServiceDep):
    try:
        return service.record_for_sensor(sensor_id, reading.sensor_id, reading.value, reading.unit)
    except SensorMismatchError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


# GET /readings/{id}  -> 200
@router.get("/readings/{reading_id}", response_model=SensorReadingOut)
def get_reading(reading_id: int, service: ReadingServiceDep):
    try:
        return service.get(reading_id)
    except ReadingNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


# PATCH /readings/{id}  -> 200
@router.patch("/readings/{reading_id}", response_model=SensorReadingOut)
def update_reading(reading_id: int, patch: SensorReadingUpdate, service: ReadingServiceDep):
    try:
        return service.update_partial(reading_id, value=patch.value, unit=patch.unit)
    except ReadingNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


# DELETE /readings/{id}  -> 204 (desactivar, no borrar)
@router.delete("/readings/{reading_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reading(reading_id: int, service: ReadingServiceDep):
    try:
        service.deactivate(reading_id)
    except ReadingNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))