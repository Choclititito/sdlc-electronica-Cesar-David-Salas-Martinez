"""main.py
Dia 5
Codigo que sirve para crear y configurar la API"""

# Importacion de librerias
from fastapi import FastAPI

from app.db import Base, engine
from app.routers import readings, sensors

# Creacion de las tablas si no existen
Base.metadata.create_all(bind=engine)

# Registro de los routers para poder acceder a las rutas de la API
app = FastAPI(title="SensorHub API", version="0.1.0")
app.include_router(sensors.router)
app.include_router(readings.router)


# Creacion de la ruta para verificar el estado de la API
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
