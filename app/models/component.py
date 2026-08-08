"""components.py
Dia 2"""

# Importancdo los modulos necesarios
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column
from datetime import datetime

# Creacion de la base de datos y la sesion
engine = create_engine("sqlite:///sdlc_electronica.db")
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


# Creacion de la clase base para los modelos
class Base(DeclarativeBase): ...


# Creacion del modelo de componentes
# Tiene varios atributos que representarian sus datos
class ComponentModel(Base):
    __tablename__ = "components"
    id: Mapped[int] = mapped_column(primary_key=True)
    part_number: Mapped[str] = mapped_column(index=True)
    component_type: Mapped[str]
    value: Mapped[float]
    unit: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
