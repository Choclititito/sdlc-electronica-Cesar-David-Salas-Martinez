from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.dependencies import (
    AlertRepositoryDep,
    ReadingRepositoryDep,
    SensorRepositoryDep,
)
from app.logging_config import configure_logging
from app.routers import alerts, readings, sensors

configure_logging()

app = FastAPI(title="SensorHub API", version="1.1.0")
app.include_router(sensors.router)
app.include_router(readings.router)
app.include_router(alerts.router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Manejo global: cualquier excepcion no controlada se convierte en un
    500 limpio, sin exponer el traceback al cliente."""
    import logging

    logging.getLogger("app").exception(
        "Error no manejado en %s %s", request.method, request.url.path
    )
    return JSONResponse(
        status_code=500, content={"detail": "Error interno del servidor"}
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics")
def metrics(
    sensor_repo: SensorRepositoryDep,
    reading_repo: ReadingRepositoryDep,
    alert_repo: AlertRepositoryDep,
) -> dict[str, int]:
    return {
        "active_sensors": sensor_repo.count_active(),
        "total_readings": reading_repo.count_all(),
        "open_alerts": alert_repo.count_open(),
    }
