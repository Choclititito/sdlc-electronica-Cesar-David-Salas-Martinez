""" dependencies.py
    Dia 5
    Codigo para definir las dependencias de la aplicacion
    Este arma la cadena get_db → repositorio → servicio en cada peticion
"""

# Importaciones 
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.repositories.reading_repository import ReadingRepository, SqlAlchemyReadingRepository
from app.repositories.sensor_repository import SensorRepository, SqlAlchemySensorRepository
from app.services.reading_service import ReadingService
from app.services.sensor_service import SensorService

# Funcion para obtener el repositorio de lecturas, inyectando la sesion de base de datos
def get_reading_repository(db: Session = Depends(get_db)) -> ReadingRepository:
    return SqlAlchemyReadingRepository(db)

# Funcion para obtener el repositorio de sensores, inyectando la sesion de base de datos
def get_sensor_repository(db: Session = Depends(get_db)) -> SensorRepository:
    return SqlAlchemySensorRepository(db)

# Funcion para obtener el servicio de lecturas, inyectando el repositorio de lecturas
def get_reading_service(
    repo: ReadingRepository = Depends(get_reading_repository),
) -> ReadingService:
    return ReadingService(repo)

# Funcion para obtener el servicio de sensores, inyectando el repositorio de sensores
def get_sensor_service(
    repo: SensorRepository = Depends(get_sensor_repository),
) -> SensorService:
    return SensorService(repo)

# Tipos de dependencias para inyectar en los endpoints
ReadingServiceDep = Annotated[ReadingService, Depends(get_reading_service)]
SensorServiceDep = Annotated[SensorService, Depends(get_sensor_service)]