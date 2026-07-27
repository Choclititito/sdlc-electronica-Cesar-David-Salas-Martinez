# Product Backlog — Sistema de Monitoreo IoT para Bodega Industrial

**Contexto del sistema:** 10 sensores de temperatura y humedad, muestreo cada 30 segundos, detección de anomalías (Temperatura > 35 °C o Humedad > 80%) y generación de alertas.

**Leyenda MoSCoW:** M = Must have | S = Should have | C = Could have | W = Won't have (esta vez)
**Story Points:** escala Fibonacci (1, 2, 3, 5, 8, 13)

---

## HU-01 — Ingesta de lecturas de sensores

**Como** sistema de monitoreo
**Quiero** recibir y almacenar las lecturas de temperatura y humedad de los 10 sensores cada 30 segundos
**Para** contar con datos actualizados y confiables para el análisis de anomalías

**Prioridad MoSCoW:** Must have
**Story Points:** 8

```gherkin
Característica: Ingesta de lecturas de sensores

  Escenario: Recepción exitosa de una lectura
    Dado que el sensor "S01" está activo y conectado
    Cuando el sensor envía una lectura de temperatura y humedad
    Entonces el sistema almacena la lectura con su marca de tiempo
    Y la lectura queda disponible para el módulo de análisis en menos de 2 segundos

  Escenario: Lectura fuera de rango físico plausible
    Dado que un sensor envía un valor de temperatura de -50 °C
    Cuando el sistema recibe el dato
    Entonces el sistema marca la lectura como "dato inválido"
    Y no la utiliza para el cálculo de anomalías

  Esquema del escenario: Frecuencia de muestreo constante
    Dado que el sensor "<sensor_id>" está operativo
    Cuando transcurren 30 segundos desde la última lectura
    Entonces el sistema recibe una nueva lectura del sensor "<sensor_id>"

    Ejemplos:
      | sensor_id |
      | S01       |
      | S05       |
      | S10       |
```

---

## HU-02 — Detección de anomalía por temperatura alta

**Como** responsable de operaciones de la bodega
**Quiero** que el sistema detecte automáticamente cuando la temperatura supera 35 °C
**Para** poder actuar antes de que se dañe la mercancía almacenada

**Prioridad MoSCoW:** Must have
**Story Points:** 5

```gherkin
Característica: Detección de anomalía de temperatura

  Escenario: Temperatura supera el umbral
    Dado que el sensor "S03" reporta una temperatura de 35.1 °C
    Cuando el sistema procesa la lectura
    Entonces el sistema genera un evento de anomalía de tipo "temperatura alta"

  Escenario: Temperatura en el límite exacto
    Dado que el sensor "S03" reporta una temperatura de 35.0 °C 
    Cuando el sistema procesa la lectura
    Entonces el sistema NO genera un evento de anomalía
    Porque el umbral se activa solo cuando el valor es estrictamente mayor a 35 °C

  Escenario: Temperatura vuelve a la normalidad
    Dado que existe una anomalía activa de "temperatura alta" para el sensor "S03"
    Cuando el sensor reporta una temperatura de 33 °C
    Entonces el sistema cierra automáticamente el evento de anomalía
```

---

## HU-03 — Detección de anomalía por humedad alta

**Como** responsable de operaciones de la bodega
**Quiero** que el sistema detecte cuando la humedad relativa supera el 80%
**Para** prevenir condensación y moho en los productos almacenados

**Prioridad MoSCoW:** Must have
**Story Points:** 5

```gherkin
Característica: Detección de anomalía de humedad

  Escenario: Humedad supera el umbral
    Dado que el sensor "S07" reporta una humedad relativa de 81%
    Cuando el sistema procesa la lectura
    Entonces el sistema genera un evento de anomalía de tipo "humedad alta"

  Escenario: Humedad justo por debajo del umbral
    Dado que el sensor "S07" reporta una humedad relativa de 79.9%
    Cuando el sistema procesa la lectura
    Entonces el sistema NO genera ningún evento de anomalía
```

---

## HU-04 — Envío de alertas en tiempo real

**Como** encargado de turno
**Quiero** recibir una alerta inmediata cuando se detecte una anomalía
**Para** poder responder rápidamente y evitar pérdidas

**Prioridad MoSCoW:** Must have
**Story Points:** 8

```gherkin
Característica: Notificación de alertas

  Escenario: Alerta enviada por correo y notificación push
    Dado que se genera un evento de anomalía en el sensor "S02"
    Cuando el sistema procesa el evento
    Entonces se envía una notificación push a los usuarios suscritos
    Y se envía un correo electrónico con el detalle de la anomalía en menos de 60 segundos

  Escenario: Evitar alertas duplicadas
    Dado que ya existe una alerta activa para el sensor "S02" por "temperatura alta"
    Cuando el sensor sigue reportando temperaturas superiores a 35 °C
    Entonces el sistema no genera una nueva alerta duplicada
    Y actualiza el evento existente con la lectura más reciente
```

---

## HU-05 — Panel de monitoreo en tiempo real (dashboard)

**Como** encargado de turno
**Quiero** visualizar en un panel el estado actual de los 10 sensores
**Para** tener una vista general del estado de la bodega en todo momento

**Prioridad MoSCoW:** Should have
**Story Points:** 8

```gherkin
Característica: Dashboard en tiempo real

  Escenario: Visualización del estado normal
    Dado que todos los sensores reportan valores dentro de rango
    Cuando el usuario abre el dashboard
    Entonces cada sensor se muestra en color verde con su última lectura

  Escenario: Visualización de sensor en anomalía
    Dado que el sensor "S04" tiene una anomalía activa
    Cuando el usuario abre el dashboard
    Entonces el sensor "S04" se muestra en color rojo
    Y se muestra el tipo de anomalía y la hora en que inició
```

---

## HU-06 — Histórico y reportes de anomalías

**Como** gerente de la bodega
**Quiero** consultar un histórico de anomalías por sensor y rango de fechas
**Para** analizar tendencias y tomar decisiones de mantenimiento

**Prioridad MoSCoW:** Should have
**Story Points:** 5

```gherkin
Característica: Histórico de anomalías

  Escenario: Consulta de histórico por rango de fechas
    Dado que existen anomalías registradas entre el 1 y el 30 de junio
    Cuando el usuario filtra el histórico por ese rango de fechas
    Entonces el sistema muestra la lista de anomalías ocurridas en ese periodo

  Escenario: Exportar reporte
    Dado que el usuario visualiza un histórico de anomalías
    Cuando selecciona la opción "Exportar a CSV"
    Entonces el sistema genera un archivo descargable con los datos filtrados
```

---

## HU-07 — Detección de sensor caído o sin comunicación

**Como** responsable de mantenimiento
**Quiero** que el sistema detecte si un sensor deja de enviar datos
**Para** distinguir entre una anomalía ambiental y una falla de hardware o conectividad

**Prioridad MoSCoW:** Must have
**Story Points:** 5

```gherkin
Característica: Detección de sensor sin comunicación

  Escenario: Sensor deja de reportar
    Dado que el sensor "S09" enviaba lecturas cada 30 segundos
    Cuando transcurren más de 90 segundos sin recibir una nueva lectura
    Entonces el sistema marca al sensor "S09" como "sin comunicación"
    Y genera una alerta de tipo "fallo de conectividad"

  Escenario: Sensor recupera comunicación
    Dado que el sensor "S09" está marcado como "sin comunicación"
    Cuando el sistema recibe una nueva lectura válida de "S09"
    Entonces el sistema cambia el estado del sensor a "activo"
```


---

## HU-08 — Escalamiento de alertas no atendidas

**Como** gerente de la bodega
**Quiero** que las alertas no reconocidas por el encargado de turno se escalen automáticamente
**Para** asegurar que ninguna anomalía crítica quede sin respuesta

**Prioridad MoSCoW:** Could have
**Story Points:** 8

```gherkin
Característica: Escalamiento de alertas

  Escenario: Alerta sin reconocer durante 10 minutos
    Dado que existe una alerta activa de "temperatura alta" sin reconocer
    Cuando transcurren 10 minutos sin que ningún usuario la marque como "atendida"
    Entonces el sistema envía una notificación al gerente de la bodega

  Escenario: Alerta reconocida a tiempo
    Dado que existe una alerta activa
    Cuando el encargado de turno la marca como "atendida" antes de 10 minutos
    Entonces el sistema no realiza ningún escalamiento
```

---

## HU-09 — Autodiagnóstico y calibración de sensores

**Como** técnico de mantenimiento
**Quiero** poder ejecutar un autodiagnóstico remoto de cada sensor
**Para** verificar su correcto funcionamiento sin necesidad de desplazarme físicamente

**Prioridad MoSCoW:** Could have
**Story Points:** 5

```gherkin
Característica: Autodiagnóstico de sensores

  Escenario: Diagnóstico exitoso
    Dado que el técnico solicita un autodiagnóstico del sensor "S08"
    Cuando el sensor responde correctamente a la señal de prueba
    Entonces el sistema muestra el estado "sensor operativo"

  Escenario: Diagnóstico fallido
    Dado que el técnico solicita un autodiagnóstico del sensor "S08"
    Cuando el sensor no responde en 15 segundos
    Entonces el sistema muestra el estado "sensor con posible falla"
    Y sugiere una revisión física
```

---

## HU-10 — Aplicación móvil de solo consulta

**Como** encargado de turno
**Quiero** consultar el estado de los sensores desde una aplicación móvil
**Para** monitorear la bodega incluso cuando no estoy frente a una computadora

**Prioridad MoSCoW:** Won't have (esta vez)
**Story Points:** 13

```gherkin
Característica: Consulta desde aplicación móvil

  Escenario: Visualización de estado general
    Dado que el usuario abre la aplicación móvil
    Cuando inicia sesión correctamente
    Entonces visualiza el estado actual de los 10 sensores

  Escenario: Recepción de alertas push en el móvil
    Dado que el usuario tiene la aplicación instalada y sesión iniciada
    Cuando se genera una nueva anomalía
    Entonces recibe una notificación push en su dispositivo móvil
```

---

## Resumen del Backlog

| ID | Historia | MoSCoW | Story Points |
|----|----------|--------|---------------|
| HU-01 | Ingesta de lecturas de sensores | Must | 8 |
| HU-02 | Detección de anomalía de temperatura | Must | 5 |
| HU-03 | Detección de anomalía de humedad | Must | 5 |
| HU-04 | Envío de alertas en tiempo real | Must | 8 |
| HU-05 | Dashboard en tiempo real | Should | 8 |
| HU-06 | Histórico y reportes de anomalías | Should | 5 |
| HU-07 | Detección de sensor caído | Must | 5 |
| HU-08 | Escalamiento de alertas | Could | 8 |
| HU-09 | Autodiagnóstico y calibración | Could | 5 |
| HU-10 | App móvil de consulta | Won't | 13 |

**Total de historias:** 12 | **Total story points:** 80
