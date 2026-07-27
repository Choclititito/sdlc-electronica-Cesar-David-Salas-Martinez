# Sprint 1 Planning — Sistema de Monitoreo IoT para Bodega Industrial

**Duración del sprint:** 2 semanas
**Equipo:** 1 desarrollador (rol combinado: Dev / Scrum Master / parte de Product Owner)
**Capacidad estimada:** ~35-38 story points (ajustado a desarrollador único)

---

## 🎯 Sprint Goal

> **Establecer el pipeline mínimo viable de monitoreo: el sistema debe ser capaz de recibir las lecturas de los 10 sensores cada 30 segundos, detectar automáticamente anomalías de temperatura (>35 °C) y humedad (>80%) con umbrales configurables, notificar dichas anomalías en tiempo real, y distinguir una anomalía ambiental real de una falla de comunicación del sensor.**

Este objetivo se centra en el **núcleo funcional** del producto (ingesta → detección → alerta) porque sin él ninguna otra funcionalidad (dashboard, históricos, reportes) tiene datos confiables sobre los cuales operar.

---

## 📋 Historias seleccionadas para el Sprint 1

| ID | Historia | MoSCoW | Story Points |
|----|----------|--------|---------------|
| HU-01 | Ingesta de lecturas de sensores | Must | 8 |
| HU-02 | Detección de anomalía de temperatura | Must | 5 |
| HU-03 | Detección de anomalía de humedad | Must | 5 |
| HU-04 | Envío de alertas en tiempo real | Must | 8 |
| HU-07 | Detección de sensor caído o sin comunicación | Must | 5 |

**Total: 5 historias — 31 story points**

### Justificación de la selección

- **HU-01 (Ingesta)** es la base de todo el sistema: sin datos confiables llegando cada 30 s, ninguna otra historia puede validarse. Se incluye primero por dependencia técnica directa.
- **HU-02 y HU-03 (Detección de anomalías)** son el valor central del producto según el contexto del negocio (evitar pérdida de mercancía por temperatura/humedad). Dependen directamente de HU-01.
- **HU-04 (Alertas en tiempo real)** cierra el ciclo de valor mínimo: detectar una anomalía sin notificarla no genera ninguna acción útil para el encargado de turno.
- **HU-07 (Sensor caído)** se incluye en este sprint (y no después) porque, sin esta lógica, un sensor desconectado se interpretaría como "todo normal" (falso negativo), lo cual es un riesgo operativo serio para un sistema de seguridad de inventario.

---

## 🔨 Desglose de tareas (≤ 4 horas)

### HU-01 — Ingesta de lecturas de sensores (Total: 18h)
| Tarea | Estimación |
| :--- | :--- |
| Definir esquema de datos de la lectura (sensor_id, timestamp, temp, humedad) | 2h |
| Implementar endpoint/broker de recepción (ej. MQTT topic por sensor) | 4h |
| Implementar validación de rango físico plausible (-40 a 80 °C, 0-100%) | 3h |
| Implementar persistencia de lecturas en base de datos time-series | 4h |
| Escribir pruebas automatizadas de los escenarios Gherkin de HU-01 | 3h |
| Prueba de carga: simular 10 sensores enviando cada 30s por 1h | 2h |

### HU-02 — Detección de anomalía de temperatura (Total: 8h)
| Tarea | Estimación |
| :--- | :--- |
| Implementar función de evaluación de umbral de temperatura | 2h |
| Implementar máquina de estados de anomalía (abrir/cerrar evento) | 4h |
| Escribir pruebas automatizadas de los escenarios Gherkin de HU-02 | 2h |

### HU-03 — Detección de anomalía de humedad (Total: 4h)
| Tarea | Estimación |
| :--- | :--- |
| Implementar función de evaluación de umbral de humedad (reutilizando lógica de HU-02) | 2h |
| Escribir pruebas automatizadas de los escenarios Gherkin de HU-03 | 2h |

### HU-04 — Envío de alertas en tiempo real (Total: 15h)
| Tarea | Estimación |
| :--- | :--- |
| Diseñar modelo de evento de alerta (tipo, sensor, severidad, estado) | 2h |
| Integrar servicio de envío de correo electrónico | 3h |
| Integrar servicio de notificaciones push | 4h |
| Implementar lógica de deduplicación de alertas activas | 3h |
| Escribir pruebas automatizadas de los escenarios Gherkin de HU-04 | 3h |

### HU-07 — Detección de sensor caído o sin comunicación (Total: 9h)
| Tarea | Estimación |
| :--- | :--- |
| Implementar job de verificación periódica de "último dato recibido" por sensor | 3h |
| Implementar transición de estado "activo" → "sin comunicación" (>90s) | 2h |
| Implementar alerta de tipo "fallo de conectividad" reutilizando HU-04 | 2h |
| Escribir pruebas automatizadas de los escenarios Gherkin de HU-07 | 2h |

**Total estimado de tareas: ~54 horas** (consistente con un sprint de 2 semanas para un desarrollador único, considerando ~6-7h/día productivas más reserva para imprevistos y reuniones).

---

## ✅ Definition of Done (DoD)

Una historia de usuario se considera **terminada** en este sprint solo si cumple **todos** los siguientes criterios:

1. **Código implementado** y subido a la rama principal mediante pull request (auto-revisión checklist, dado el equipo de un solo desarrollador).
2. **Todos los escenarios Gherkin** de la historia están automatizados y pasan en verde (100%).
3. **Pruebas unitarias** de la lógica de negocio con cobertura ≥ 80% en los módulos nuevos.
4. **Sin errores críticos ni bloqueantes** conocidos (severidad alta) abiertos para esa historia.
5. **Manejo de errores** implementado para los casos límite descritos en los escenarios (datos inválidos, timeouts, valores fuera de rango).
6. **Desplegado y verificado en entorno de staging**, no solo en local.
7. **Documentación técnica mínima actualizada** (README del módulo o comentarios de configuración, endpoints/topics usados).
8. **Validación funcional manual** contra el Sprint Goal: la historia contribuye de forma verificable al flujo ingesta → detección → alerta.
9. **Aceptación registrada** por el rol de Product Owner (autoevaluación explícita contra los criterios de aceptación de la historia, no solo "parece funcionar").

**Nota:** ninguna historia se marca como "Done" si solo cumple parcialmente estos criterios (p. ej. código sin pruebas automatizadas) — en ese caso permanece "In Progress" y se re-evalúa en el Sprint Review para decidir si pasa al siguiente sprint.
