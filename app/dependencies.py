""" dependencies.py
    Dia 4        """

#Importaciones de los modulos necesarios
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.repositories.reading_repository import ReadingRepository, SqlAlchemyReadingRepository
from app.services.reading_service import ReadingService

# Definimos las dependencias para el repositorio y el servicio de lecturas
def get_reading_repository(db: Session = Depends(get_db)) -> ReadingRepository:
    return SqlAlchemyReadingRepository(db)


def get_reading_service(
    repo: ReadingRepository = Depends(get_reading_repository),
) -> ReadingService:
    return ReadingService(repo)


ReadingServiceDep = Annotated[ReadingService, Depends(get_reading_service)]