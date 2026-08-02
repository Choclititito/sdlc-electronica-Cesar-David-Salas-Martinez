from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.repositories.reading_repository import ReadingRepository, SqlAlchemyReadingRepository
from app.repositories.sensor_repository import SensorRepository, SqlAlchemySensorRepository
from app.services.reading_service import ReadingService
from app.services.sensor_service import SensorService


def get_reading_repository(db: Session = Depends(get_db)) -> ReadingRepository:
    return SqlAlchemyReadingRepository(db)


def get_sensor_repository(db: Session = Depends(get_db)) -> SensorRepository:
    return SqlAlchemySensorRepository(db)


def get_reading_service(
    repo: ReadingRepository = Depends(get_reading_repository),
) -> ReadingService:
    return ReadingService(repo)


def get_sensor_service(
    repo: SensorRepository = Depends(get_sensor_repository),
) -> SensorService:
    return SensorService(repo)


ReadingServiceDep = Annotated[ReadingService, Depends(get_reading_service)]
SensorServiceDep = Annotated[SensorService, Depends(get_sensor_service)]