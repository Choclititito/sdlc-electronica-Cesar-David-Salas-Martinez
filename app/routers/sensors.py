from fastapi import APIRouter, HTTPException, Query, status
from app.dependencies import SensorServiceDep
from app.schemas.sensor import SensorIn, SensorOut, SensorUpdate
from app.services.exceptions import SensorNotFoundError, SensorAlreadyExistsError

router = APIRouter(prefix="/sensors", tags=["sensors"])


@router.get("", response_model=list[SensorOut])
def list_sensors(
    service: SensorServiceDep,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    return service.list(limit, offset)


@router.post("", response_model=SensorOut, status_code=status.HTTP_201_CREATED)
def create_sensor(sensor: SensorIn, service: SensorServiceDep):
    try:
        return service.register(sensor.sensor_id, sensor.sensor_type.value, sensor.unit)
    except SensorAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/{sensor_id}", response_model=SensorOut)
def get_sensor(sensor_id: str, service: SensorServiceDep):
    try:
        return service.get(sensor_id)
    except SensorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.patch("/{sensor_id}", response_model=SensorOut)
def update_sensor(sensor_id: str, patch: SensorUpdate, service: SensorServiceDep):
    try:
        sensor_type = patch.sensor_type.value if patch.sensor_type else None
        return service.update_partial(sensor_id, sensor_type, patch.unit)
    except SensorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.delete("/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor(sensor_id: str, service: SensorServiceDep):
    try:
        service.deactivate(sensor_id)
    except SensorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))