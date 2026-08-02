""" readings.py
    Dia 3        """

#Importaciones de los modulos
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

#Importamos el modelo base de la base de datos
from app.db import Base

# Aqui se ve como vamos a leer los datos de los sensores
class ReadingModel(Base):
    __tablename__ = "readings"
    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[str] = mapped_column(index=True)
    value: Mapped[float]
    unit: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)