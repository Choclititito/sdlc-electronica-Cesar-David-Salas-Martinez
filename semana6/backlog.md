# Backlog — SensorHub Final

## Épica: RF-1 CRUD de sensores (ubicación)
- [ ] Agregar campo `location: Mapped[str | None]` a SensorModel
- [ ] Actualizar SensorIn/SensorOut/SensorUpdate en schemas
- [ ] Migracion de Alembic

## Épica: RF-5 Gestión de alertas (estado open/acknowledged/resolved)
- [ ] Diseñar estado como Enum, en dominio puro, TDD — martes
- [ ] Agregar campo status a AlertModel + migracion
- [ ] Endpoint PATCH /alerts/{id} para cambiar estado
- [ ] GET /sensors/{id}/alerts con filtro opcional ?status=open

## Épica: RF-6 Estadísticas por sensor y periodo
- [ ] Servicio de agregación (min/max/promedio), TDD, dominio puro — martes
- [ ] Endpoint GET /sensors/{id}/readings/stats?from=&to=
- [ ] Agregación en BD via func.min/max/avg (no en Python)

## Épica: RF-7 Health + métricas básicas
- [ ] Definir métricas: sensores activos, total lecturas, alertas abiertas
- [ ] Endpoint GET /metrics

## Épica: RNF-5 Logs estructurados + manejo global de errores
- [ ] Logging en JSON
- [ ] Exception handler global en FastAPI

## Épica: RNF-6 Documentación
- [ ] Estudiar sintaxis de Mermaid (~30 min) — https://mermaid.js.org/intro/
- [ ] Diagrama de arquitectura del proyecto en Mermaid, embebido en README
      (recomendado: diagrama de capas — routers -> services -> repositories
      -> models, o un diagrama de flujo de una peticion tipo POST reading)
- [ ] ADR 0002 (candidato: estrategia de notificacion/OCP, o decision de
      estado de alertas)
- [ ] Consolidar AI_LOG.md

## Épica: Limpieza / Integración 
- [ ] Investigar y decidir sobre app/models/component.py
- [ ] Confirmar Docker + Compose + Alembic funcionando end-to-end
- [ ] CI en verde con todo lo nuevo
- [ ] Deploy final a Render, probar RF en URL publica