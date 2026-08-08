"""db.py
Dia 4
Codigo que sirve para crear y configurar la base de datos"""

# Importaciones de los modulos
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Creacion de la base de datos y la sesion para poder interactuar con ella
engine = create_engine("sqlite:///sdlc_electronica.db")
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


# Creacion de la clase base para poder crear las tablas de la base de datos
class Base(DeclarativeBase): ...


# Creacion de la funcion para poder obtener la sesion de la base de datos
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
