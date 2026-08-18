from fastapi import APIRouter, Query

from app.dependencies import AlertQueryServiceDep
from app.models.alert import AlertModel
from app.schemas.alert import AlertOut

router = APIRouter(tags=["alerts"])


@router.get("/sensors/{sensor_id}/alerts", response_model=list[AlertOut])
def list_alerts(
    sensor_id: str,
    service: AlertQueryServiceDep,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> list[AlertModel]:
    return service.list_for_sensor(sensor_id, limit=limit, offset=offset)
