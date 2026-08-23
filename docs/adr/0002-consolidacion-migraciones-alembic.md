# ADR 0002: Consolidacion del historial de migraciones de Alembic

## Estado
Aceptado (decision ya tomada y en uso).

## Contexto
Durante la semana final del proyecto, migrations/env.py nunca importaba
AlertModel (quedo pendiente desde que se creo ese modelo, en una sesion
posterior a la reconstruccion de Alembic tras un incidente de merge
anterior). Esto causaba que Alembic desconociera por completo la tabla
`alerts` en sus comparaciones de autogenerate: al intentar generar una
migracion para agregar los campos `severity`/`status`, Alembic proponia
recrear la tabla `alerts` completa desde cero, como si nunca hubiera
existido, en vez de generar un `ALTER TABLE` incremental correcto.

Se evaluaron dos caminos: (a) corregir el import y generar una migracion
incremental más sobre el historial existente de 3 archivos, o (b) borrar
el historial completo y generar una unica migracion consolidada que
describa el esquema completo actual.

## Decision
Se opto por (b): consolidar las 3 migraciones previas
(`605f5409018b`, `e9b12090ca8e`, `d8afeb2fe3fe`) en una unica migracion
(`4e33ea8ef589`) que crea las 3 tablas completas (sensors, readings,
alerts) con todos los campos vigentes a la fecha, generada contra una
base de datos completamente vacia.

## Consecuencias

+ Historial de migraciones simple y confiable de leer: una sola
  revision describe el esquema completo, sin arrastrar la inconsistencia
  de que `alerts` "aparece" en una migracion tardia por un descuido
  de configuracion.
+ Se evito seguir generando migraciones sobre una base ya corrupta
  (el archivo incremental generado antes de la consolidacion proponia
  incorrectamente un `CREATE TABLE alerts` sobre una tabla que ya
  existia).

- Costo operativo real en produccion: cualquier base de datos que ya
  tuviera aplicado el historial viejo (Render, en este caso) queda con
  su tabla `alembic_version` apuntando a una revision que ya no existe
  en el codigo (`d8afeb2fe3fe`). El deploy fallo con
  `Can't locate revision identified by 'd8afeb2fe3fe'` hasta que se
  reseteo manualmente la base de datos de produccion (DROP de las 4
  tablas via conexion directa con psql, seguido de un redeploy).
- Se perdieron los datos de prueba que existian en la base de datos de
  Render al momento del reset — aceptable en este contexto de curso,
  pero esta decision seria mucho mas costosa (o inviable sin trabajo
  adicional de migracion de datos) en un sistema con datos reales de
  usuarios.
- Establece un precedente: consolidar el historial de migraciones no
  es una operacion "gratis" una vez que existe cualquier entorno
  desplegado con el historial anterior aplicado — requiere coordinacion
  manual explicita, no solo un push.
