""" db.py
    Dia 3        """

#Importaciones de los modulos
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

#Creamos la base de datos y la sesion para poder hacer las consultas
engine = create_engine("sqlite:///sdlc_electronica.db")
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

#Creamos la clase base para poder crear los modelos de la base de datos
class Base(DeclarativeBase): ...