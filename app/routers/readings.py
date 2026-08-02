from datetime import datetime
from fastapi import APIRouter, HTTPException, Query, status
from app.dependencies import ReadingServiceDep, SensorServiceDep
from app.schemas.reading import SensorReadingIn, SensorReadingOut, SensorReadingUpdate
from app.services.exceptions import (
    ReadingNotFoundError, SensorMismatchError, InvalidDateRangeError, SensorNotFoundError,
)

router = APIRouter(tags=["readings"])


@router.get("/sensors/{sensor_id}/readings", response_model=list[SensorReadingOut])
def list_readings(
    sensor_id: str,
    service: ReadingServiceDep,
    sensor_service: SensorServiceDep,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    from_: datetime | None = Query(None, alias="from"),
    to: datetime | None = Query(None),
):
    try:
        sensor_service.get(sensor_id)  # 404 si el sensor no existe
        return service.history(sensor_id, limit=limit, offset=offset, date_from=from_, date_to=to)
    except SensorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidDateRangeError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


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
):
    try:
        sensor_service.get(sensor_id)  # 404 si el sensor no existe
        return service.record_for_sensor(sensor_id, reading.sensor_id, reading.value, reading.unit)
    except SensorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except SensorMismatchError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/readings/{reading_id}", response_model=SensorReadingOut)
def get_reading(reading_id: int, service: ReadingServiceDep):
    try:
        return service.get(reading_id)
    except ReadingNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.patch("/readings/{reading_id}", response_model=SensorReadingOut)
def update_reading(reading_id: int, patch: SensorReadingUpdate, service: ReadingServiceDep):
    try:
        return service.update_partial(reading_id, value=patch.value, unit=patch.unit)
    except ReadingNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.delete("/readings/{reading_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reading(reading_id: int, service: ReadingServiceDep):
    try:
        service.deactivate(reading_id)
    except ReadingNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))