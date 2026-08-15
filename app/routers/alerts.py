from fastapi import APIRouter

from app.dependencies import AlertRepositoryDep
from app.models.alert import AlertModel  # <-- agrega este import
from app.schemas.alert import AlertOut

router = APIRouter(tags=["alerts"])


@router.get("/sensors/{sensor_id}/alerts", response_model=list[AlertOut])
def list_alerts(sensor_id: str, repo: AlertRepositoryDep) -> list[AlertModel]:  
    #AlertModel, no AlertOut
    return repo.list_for_sensor(sensor_id)