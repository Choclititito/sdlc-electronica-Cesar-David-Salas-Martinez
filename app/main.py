from fastapi import FastAPI #Importamos FastAPI para crear la API
from pydantic import BaseModel, Field #Importamos BaseModel y Field


# Creamos la instancia de FastAPI
app = FastAPI(title="SensorHub API", version="0.1.0")
 
class SensorReadingIn(BaseModel): # Creamos la clase para simular un sensor
    sensor_id: str = Field(..., examples=["TEMP-01"])
    value: float
    unit: str = "C"
 
class SensorReadingOut(SensorReadingIn): # Creamos la clase para simular la salida de un sensor
    id: int
 
@app.get("/health") #la ruta para verificar el estado de la API
def health() -> dict[str, str]:
    return {"status": "ok"}
 
@app.post("/readings", response_model=SensorReadingOut, status_code=201)
# Creamos la ruta para recibir los datos del sensor
def create_reading(reading: SensorReadingIn) -> SensorReadingOut:
    return SensorReadingOut(id=1, **reading.model_dump())  # manana lo persistimos
