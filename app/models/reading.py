""" reading.py
    Dia 5
    Codigo para hacer que cada fila sea una medicion
    individual, amarrada a su sensor correspondiente"""

from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base

# Mapeo de la tabla, con sensor_id como llave foranea hacia sensores.sensor_id.
class ReadingModel(Base):
    #Nombre de la tabla
    __tablename__ = "readings" 
    # Definicion de las columnas de la tabla
    id: Mapped[int] = mapped_column(primary_key=True)
    # ID del sensor al que pertenece esta medicion
    sensor_id: Mapped[str] = mapped_column(ForeignKey("sensors.sensor_id"), index=True)
    # Valor de la medicion
    value: Mapped[float]
    #  Unidad de la medicion
    unit: Mapped[str]
    # Fecha y hora de la medicion
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, index=True)
    # Estado de la medicion, si esta activa o no
    is_active: Mapped[bool] = mapped_column(default=True)