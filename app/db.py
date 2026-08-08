""" db.py
    Semana 4 Dia 2 
    Soporte para PostgreSQL via DATABASE_URL, SQLite como default local"""

import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session


def get_database_url() -> str:
    """Lee DATABASE_URL del entorno; normaliza el prefijo del driver.

    Algunos proveedores (Render, Heroku, etc.) entregan la URL como
    postgres:// o postgresql:// sin el sufijo +psycopg que SQLAlchemy 2.x
    necesita para saber qué driver usar.
    """
    url = os.getenv("DATABASE_URL", "sqlite:///sensorhub.db")
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql://") and "+psycopg" not in url:
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


SQLALCHEMY_DATABASE_URL = get_database_url()

# connect_args solo aplica a SQLite (Postgres no lo necesita ni lo acepta)
connect_args = (
    {"check_same_thread": False}
    if SQLALCHEMY_DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,  # valida la conexión antes de usarla 
)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase): ...


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()