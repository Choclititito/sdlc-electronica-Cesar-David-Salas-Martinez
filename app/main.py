""" main.py
    Dia 4        """

#Importaciones
from fastapi import FastAPI
from app.db import Base, engine
from app.routers import readings


Base.metadata.create_all(bind=engine)  # crea las tablas si no existen

#creación de la app FastAPI
app = FastAPI(title="SensorHub API", version="0.1.0")
app.include_router(readings.router)

# Endpoint de salud
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}