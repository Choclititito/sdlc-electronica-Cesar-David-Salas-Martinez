from fastapi import APIRouter, HTTPException, Query
from fastapi import status as http_status

from app.dependencies import AlertQueryServiceDep
from app.domain.alert_status import AlertStatus, InvalidTransitionError
from app.models.alert import AlertModel
from app.schemas.alert import AlertOut, AlertStatusUpdate
from app.services.alert_query_service import AlertNotFoundError

router = APIRouter(tags=["alerts"])


@router.get("/sensors/{sensor_id}/alerts", response_model=list[AlertOut])
def list_alerts(
    sensor_id: str,
    service: AlertQueryServiceDep,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    status_filter: str | None = Query(None, alias="status"),
) -> list[AlertModel]:
    return service.list_for_sensor(
        sensor_id, limit=limit, offset=offset, status=status_filter
    )


@router.patch("/alerts/{alert_id}", response_model=AlertOut)
def update_alert_status(
    alert_id: int, patch: AlertStatusUpdate, service: AlertQueryServiceDep
) -> AlertModel:
    try:
        return service.change_status(alert_id, AlertStatus(patch.status))
    except AlertNotFoundError as exc:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    except InvalidTransitionError as exc:
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT, detail=str(exc)
        ) from exc
