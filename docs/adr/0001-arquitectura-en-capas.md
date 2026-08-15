# ADR 0001: Arquitectura en capas para SensorHub

## Estado
Aceptado (decisión ya tomada y en uso).

## Contexto
El código inicial vivía todo en `main.py`, mezclando FastAPI, SQLAlchemy y
Pydantic. Esto hacía las pruebas de reglas de negocio (ej. rechazar
temperaturas bajo el cero absoluto) lentas, porque requerían una base de
datos real en cada corrida. Ademas, se pidió explícitamente implementar
patrón Repositorio + capa de Servicio con `Protocol`, para permitir
repositorios fake en tests.

## Decision
Arquitectura en 4 capas: routers -> services -> repositories -> models.

- **Router**: recibe HTTP, sin lógica de negocio.
- **Service**: reglas de negocio (cero absoluto, rangos de fecha, duplicados).
- **Repository**: único lugar que toca SQL, expuesto como `Protocol` +
  implementación concreta con SQLAlchemy.
- **Model**: tablas del ORM.

`Protocol` es la pieza clave: el service no sabe si hay SQLite, PostgreSQL,
o un fake en memoria detrás del repositorio.

## Consecuencias

+ Tests de servicio rápidos, sin base de datos real (fake repository).
+ Migrar de SQLite a PostgreSQL solo requirió cambiar `DATABASE_URL`, sin
  tocar `app/services/`.
+ `mypy` + `Protocol` detectaron un bug real (`sensor_service` tipado
  contra la implementación concreta en vez del Protocol).
- Más archivos y ceremonia: un cambio pequeño toca 4-5 archivos (schema,
  service, repo, protocol, router).
- Curva de aprendizaje: la cadena de `Depends` (`get_db -> repo ->
  service`) no es obvia al inicio.