# BITACORA IA  

##  Entrada 1: Dia 2  
En este dia le di a la IA el siguiente prompt "Dame ejemplos de Gherkins en base a la idea principal que te di ", luego le volvi a pedir que me diera mas ejemplos  
De los 12 ejemplos que me dio rechaze 8, modifique 2 y acepte 2.  
La mayoria los rechaze porque agregaba puntos que sentia que se alejaban demasiado de la idea principal por ejemplo:  
Ejemplo 1: Hilos de ejecución (RTOS) y Prioridad de Tareas,  la cual tomaba como si hubiera una pantalla oled que no existia  
termine usando solamente 2 US-06: Transferencia de datos de audio directa (DMA) sin bloqueo de CPU, y US-10: Recuperación automática del sistema (Watchdog)  

##  Entrada 2: Dia 2  
Ya con la idea original de ca gherkin le di el prompt: "Hazme una critica de los gherkin que te voy a mandar, pensando “¿es verificable? ¿es ambiguo? ¿qué caso borde falta?, al final pon un resumen corto de tu critica"  
para que me diera una critica a cada gherkin que tenia, incluyendo en los que me ayudo, las criticas originales estan en el historial del backlog de este dia, con estas criticas fui e hice los cambios correspondientes.  
Ya con estos nuevos gherkin los volvi a pasar con la IA, la cual me volvio a dar una critica mas aprobatoria para estos.  

El usar la IA para hacer los gherkin no lo senti tan optimo ya que en mi caso ya que inventaba cosas que no eran compatibles entre si, y asumia cosas que no le habia dicho.  

Mientras que usarla para encontrar fallos la encontre mejor, ayudandome a encontrar cosas que se me habian pasado por alto.  


## Entrada 1: dia 3  
En este ejercicio, el prompt fue "Utiliza las siguientes instrucciones y explicamelas" adjuntando el codigo.  
Utilize los 3 codigos que me proporciono, modificando algunos detalles y comentandolos.  

## Entrada 1: dia 4  
Aqui le pedi "Dime como harias las siguientes instrucciones:"  adjuntando las instrucciones, ya que no las habia entendido del todo.  
Aqui utilice y modifique el archivo .toml para que funcionara en mi repositorio, con mi configuracion de carpetas.  
Ademas me ayudo a comprobar mi codigo que hice para el test  

## Entrada 1: dia 5 EVALUACION  

Utilice este prompt: "Necesito que hagas lo siguiente: Contexto: eres el único desarrollador de un sistema de monitoreo IoT para una bodega industrial: 10 sensores de temperatura y humedad cada 30 segundos, detección de anomalías (T > 35 °C o H > 80%) y alertas. Product Backlog: ≥ 10 user stories con Gherkin, story points y priorización MoSCoW."  
Me dio una lista de 12 casos, de los cuales acepte 10 y rechace 2.  
Rechace 
HU-07 — Configuración de umbrales de anomalía --- Ya que por el contexto proporcionado no seria necesario
HU-09 — Gestión de usuarios y roles --- Ya que al descartar la anterior no se podria modificar nada y por ende los roles no tienen uso  
Las demas las acepte y modifique para que se ajustaran a lo pedido  

## Entrada 2: dia 5 EVALUACION  
Utilice el prompt: "hazme un Sprint 1 Planning: Sprint Goal, 5–7 historias justificadas, tareas ≤ 4 h, Definition of Done"  
Aqui lo utilice eliminando las referencias a la tarea 07, quedando 5 historias, modificando las horas, modificando los story points, agregando un total de horas de cada tarea.  

## Entrada 3: dia 5 EVALUACION  
Utilice el prompt: "Necesito una Implementación TDD de ≥ 3 historias del núcleo: SensorReading, AnomalyDetector (umbrales inyectados, no hardcodeados) y AlertManager (estrategia abstracta + Console y File). Cobertura ≥ 80%"  
Aqui me dio 6 codigos, 3 test y 3 de historias de nucleo.  
Los cuales acepte, modificando la forma que importaban los demas codigos ya que daba un error al asumir una distribucion diferente.  


