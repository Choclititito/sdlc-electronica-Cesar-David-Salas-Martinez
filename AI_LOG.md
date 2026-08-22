# Bitacora de IA  
Bitacora para poner registrar el uso de la IA a partir de la semana 3, las otras 2 semanas tienen su bitacora dentro de sus carpetas.  
Se esta usando la IA "Claude" principalmente.  

# Semana 3  

## Dia 2  
Le pedi a la IA el siguiente prompt: "Explicame el siguiente codigo paso por paso", adjuntando el codigo del pdf.  
Me dio una explicacion paso a paso que me ayudo para poder recrear el codigo entendiendolo paso a paso.  

## Dia 3  
El prompt que use fue : " las indicaciones son las siguientes, patron repositorio y capa de servicio, escribe los test del servicio con un repositorio fake en memoria, sin base de datos real. Adjunto tambien el siguiente codigo" el cual es el del pdf.  

Me dio 4 codigos:  
reading.py  
reading_repository.py  
reading_service.py  
test_reading_service.py  

Los cuales termine aceptando, y comentando. pero al momento de querer probarlos tuve errores:  

Primero tuve que resolver un problema del pytest con la IA pasandole los errores que tenia, teniendo que re hacer el entorno virtual.  

Luego necesite un codigo mas para el db.py, para poder iniciar y hacer funcionar el test, lo escribi y le pedi a claude "Arregla el siguiente codigo que usare para el db.py", dandome feedback ayudandome a arreglar el codigo.  
Haciendo que ya pudiera ejecutar los tests.  

## Dia 4  
Este dia le pase el siguiente prompt: "Inyeccion de dependencia y convenciones REST: Conecta las capas con el sistema de dependencias de FastAPI (Depends) y diseña tus endpoints respetando la tabla — apréndela, te permitirá adivinar cómo consumir cualquier API bien hecha,Agrega también filtros por rango de fechas (?from=...&to=...) y maneja los errores con HTTPException y códigos correctos: 400, 404, 409, 422."  
Adjuntando la tabla  

Lo que me dio la IA fueron 10 codigos, modificando algunos de los anteriores.  


app/main.py: archivo donde se inicia toda la aplicacion.  
app/db.py: archivo para la conexion de datos sin cambios mayores.  
app/models/reading.py: archivo para la definicion de la tabla.  
app/schemas/reading.py: archivo de como entran y salen datos por HTTP.  
app/services/exceptions.py: archivo para vocabulario de errores de negocio.  
app/repositories/reading_repository.py: capa de acceso de datos con su contrato.  
app/services/reading_service.py: la logica de nogocio y las reglas del dominio.  
app/dependencies.py: donde se arma la cadena de objetos por peticion.  
app/routers/readings.py: La capa HTTP, donde traduce el mundo web al mundo del servicio.  
tests/test_reading_service.py: donde se prueba el readingservice.  

## Dia 5  
Le di el prompt que indicaba "Tomando en cuenta lo que llevo hecho ahora neceisto un API completo con:
-CRUD completo de sensores y lecturas siguiendo las convenciones REST de la tabla.  
-Validación Pydantic con física real: rechaza unidades desconocidas y valores fuera de rango físico por tipo de sensor.  
-Arquitectura en 4 capas limpiamente separadas.  
-Tests de integración con TestClient de FastAPI; cobertura ≥ 80%.  
-Swagger funcional en /docs."  

Aqui me dio diversos codigos, en los cuales hacia modificaciones en codigos anteriores y me dio algunos nuevos  

Al probar los codigos que me dio, no pasaba los pytest, por un error en el codigo, que tuve que solucionar modificando el .py de los test.  

## Dia 5 entrada 2  
Con los comentarios de mi compañero tuve que hacer unas modificaciones, preguntandole como solucionarlo, empezando con

1.-propmt:"Como hacer un migrado a la API 2.x"  
2.-propmt:"Como corrijo este codigo para tener orden con desempate"  
3.-propmt:"Ayudame a que los test tengan un 80% de cobertura"  
4.-propmt:"Como arreglo el problema de archivos autogenerados"  

Los otros puntos como el de cambiar el datatime.now, o el agregado de los __init__ se hizo sin ninguna mayor complicacion.  

# Semana 4  

## Dia 2  
En este dia le di el prompt a la IA "Explicame paso a paso las siguientes instrucciones:" insertando lo marcado en el curso, la IA me dio algunos cambios en el codigo ademas de pasos de como instalar y verificar el Alembic, como cambios en el codigo env.py para su correcto funcionamiento, y testeos para corroborar la creacion correcta de las tablas como el sqlite3 sensorhub.db ".schema readings.  

## Dia 3  
En este dia tuve dificultades, no por la tarea, si ni por problemas de ramas, al hacer la prueba para que fallara el test tuve que agregarle el ci.yml al main e intentar hacer un merge con una rama, esto para que me fallara el test, luego corregi errores para que lo lograra pasar, pero esto provoco un problema entre las diferentes versiones, que termino con que perdiera mi progreso hasta ese dia, use a la IA, para preguntarle como solucionar el problema, pasandole los comandos que salian, teniendo que rehacer gran parte y corregir errores nuevo que me salian a causa de retazos que aun quedaban del viejo codigo, apoyandome de la IA para poder solucionar todo.  

## Dia 4  
Le di el prompt a la IA "Basandote en la siguiente instruccion: (lo que indicaba el PDF), pasame formas de saber que todo funciona bien", dandome diferentes comando para verificar su funcionalidad, como comprobando desde la consola que todo si se guardara correctamente con:  
curl -X POST https://sensorhub-api-bret.onrender.com/sensors \  
  -H "Content-Type: application/json" \  
  -d '{"sensor_id":"TEMP-01","sensor_type":"temperature","unit":"C"}'  
  
curl -X POST https://sensorhub-api-bret.onrender.com/sensors/TEMP-01/readings \  
  -H "Content-Type: application/json" \  
  -d '{"value":22.5,"unit":"C"}'  
  
curl https://sensorhub-api-bret.onrender.com/sensors/TEMP-01/readings  

Sirviéndome para saber que todo estaba correcto, junto a otras pruebas  

## Dia 5  
Le di el prompt "Basandote en estos parametros, el codigo cumple con la checklist", con una imagen de estos parametros.  
Me indico con que cumplia y que cosas me faltaban, pero solo eran cosas del Readme, asi que no hubo mayor problema.  

# Semana 5  

## Dia 2  
En este dia utilizamos Aider como fue indicado, hice una prueba, ya tenia un codigo que me habia dado copilot con el promt de ejemplo, siendo el siguiente:  
#Codigo de copilot  
```python
def celsius_to_fahrenheit(c: float) -> float:
    """Convert a Celsius temperature to Fahrenheit rounded to 2 decimals.

    Args:
        c: Temperature in degrees Celsius.

    Returns:
        Temperature in degrees Fahrenheit rounded to 2 decimal places.
    """
    return round(c * 9.0 / 5.0 + 32.0, 2)
```

Abajo poniendo un comentario diciendo: #creado por aider con la API de Gemini, esto para dar el siguiente promt " Crea debajo del comentario "#creado por aider con la API de Gemini" escribe una funcion pura celsius_to_farenheit(c:float) -> float con type hints completos, docstring, sin dependencias externas, redondeo a 2 decimales"  
Todo esto para poder tener una comparativa directa entre los 2, lo malo es que lo que termino haciendo fue solamente cambiar el comentario y reescribir todo el codigo, aunque termino quedando igual, como se puede ver en el archivo.  

¿En que supera a Copilot?:  
Siento que es mejor en el hecho de poder funcionar con diferentes inteligencias artificiales, haciendo que su uso no se vea limitado solamente a una.  

¿En que falla?:  
Pues a mi me fallo en lo que le pedi, interpreto mal una instruccion que a mi parecer era bastante sencilla, y no debio haber tenido que fallar, ademas que es mas incomod de usar que el copilot que ya tiene una integracion directamente en el VSC.  

## Dia 3  
Aqui utilice la IA con Aider, con una key de gemini, usando el modelo 3.5 flash, use estos 2 prompts:  

1.-"Revisa la clase ReadingService en este archivo como un ingeniero senior en un
code review. Busca: violaciones de SOLID, casos borde sin manejar, riesgos de
seguridad y problemas de rendimiento. Para cada hallazgo indica la linea y
propon una correccion. No reescribas todo; solo señala."  

2.-"> que casos borde (nulos, limites, entradas malformadas) no estoy manejando en esta clase?"  

Estos dos prompts, me dieron resultados no tan satisfactorios, empezando con el primero, el Aider al estar diseñado para siempre modificar, termino haciendo caso omiso a mi indicacion de solamente señalar las cosas que debia modificar, por el lado amable, termine dejando las modificaciones porque las vi acertadas.  
Con el segundo tuve un problema que me indicaba que el modelo de IA no podia ser utilizado en este momento, que deberia intentar despues, a pesar que ya estaba terminando el codigo, curiosamente, checando manualmente, pude notar que si habia terminado de hacer el codigo, lo cual solo me confundio mas.  


## Dia 4  
Aqui lo que hice fue juntar una serie de notas de todo el proyecto, para asi que la IA tenga un contexto suficiente para poder hacer un ADR bueno, las notas que le di al final fueron las siguientes:

```python
- empezamos con todo junto en main.py (fastapi + sqlalchemy + pydantic
  mezclado), funcionaba pero dificil de testear

- necesitabamos probar la logica (ej. que rechace temperatura bajo cero
  absoluto) sin tener que levantar sqlite/postgres cada vez, muy lento
  para iterar

- profesor pidio explicitamente patron repositorio + capa de servicio,
  con Protocol para poder inyectar un fake repo en los tests

- capas que terminamos usando: router (recibe http, nada de logica),
  service (reglas de negocio tipo validar cero absoluto, rangos de fecha,
  duplicados), repository (unico que toca sql, expuesto como Protocol +
  implementacion concreta SqlAlchemy), model (tabla sqlalchemy)

- el Protocol es la parte clave, permite que el service no sepa si hay
  sqlite o postgres detras, ni si es un fake en memoria para tests  

- se probo en la practica: migramos de sqlite a postgres agregando
  DATABASE_URL configurable, y no tocamos nada de app/services/  

- tambien encontramos un bug real por no seguir bien el patron: un
  service (sensor_service) quedo tipado contra la clase concreta del
  repositorio en vez del Protocol, se detecto con mypy y se corrigio  

- contras que notamos: cada feature chica implica tocar como 4-5 archivos
  (schema, service, repo, protocol, router), mas ceremonia que tener todo
  junto  

- tambien mas curva de aprendizaje, la inyeccion de dependencias
  encadenada (get_db -> repo -> service via Depends) no es obvia al
  principio  

- decision ya esta tomada y en uso, no es hipotetica  
```
Con todas estas notas la IA de gemini me dio un ADR, bastante completo, pero con pequeños ajustes que tuve que hacer:  
- Titulo muy largo: ADR 001: Adopción de Arquitectura en Capas y Patrón Repositorio con Inyección de Dependencias  

- Tamaño muy grande del ADR: 47 renglones en total   

- Mal redactado: Seguridad de Tipos Estáticos  

Con estas correcciones, y haciendo una clase de resumen de esta pude tener una mejor ADR.



## Dia 5  

Prompts usados:  
"Escribe tests para un AnomalyDetectionService que evalue una lectura 
contra thresholds min/max de un sensor, usando fakes para repo y notifier, 
antes de implementar el servicio (TDD estricto)"  
" Realiza los codigos para poder implementar esta nueva funcion al codigo, tomando en cuenta la estrategia de alerta intercambiable(OCP), explica cada codigo que me termines pasando"  
La IA me paso varios tests y los codigos que le pedi, tenian errores que evitaban que pudieran funcionar como deberian empezando con falta de importaciones de librerias, en el codigo de routers/readings.py, problemas con el ruff, teniendo errores de formato en su mayoria, como lineas muy largas o mal formato de las librerias, el mypy tambien detecto errores que tuve que corregir, como el tener que agregar el AlertRepositoryDep = ... y el AnomalyDetectionServiceDep = ... en el archivo de app/dependencies.py, y por ultimo los pytest fueron los unicos que funcionaron sin problema.  

## Dia 6  

En este dia verificamos lo que tuvimos que hacer fue revisar el PR de nuestro compañero, primero nosotros, y luego pedirle ayuda a la IA, lo que note fue como la IA ayuda mucho a encontrar fallos mas centrados en el codigo, mientras que no puede checar tanto errores verificables en el servidor montado, ya que no tiene la capacidad de poder hacer un servidor propio para poder verificarlo, tambien es mas facil para mi tener criterio si se entiende la descripccion o titulo del PR, ya que una inteligencia artificial, casi siempre va a tener errores de redaccion, y va complicado que sepa si es entendible para un humano.


# Semana 6 PROYECTO  

## Entrada 1:  
En la primera entrada, le pregunte a la IA basandose en las instrucciones el siguiente prompt "Basandote en esta lista de requisitos, en cuales puntos no tengo todo completado", adjuntando las 2 listas de requisitos, para asi tener una lista de cosas que me podrian faltar, me termino dando varios puntos que le faltaban a mi proyecto, los cuales en su mayoria accedi a hacer.  

## Entrada 2:  
Le di el prompt: "Necesito una funcion pura determine_severity(value, min_threshold,
max_threshold) que devuelva WARNING o CRITICAL segun que tan lejos esta
el valor del threshold, o None si esta en rango. Sigue TDD: dame primero
los tests, sin implementacion todavia."  

Me genero varios tests, los cuales funcionaron como deberian, saliendo con resultados rojos.  

Luego tuve que usar un prompt que indicaba : "Diseña un Enum AlertStatus (open, acknowledged, resolved) y una funcion
can_transition(current, target) que valide transiciones. resolved debe
ser terminal. Dame los tests primero, TDD estricto."  

Me dio los tests , de los cuales no tuve que cambiar mucho, mas que algunos detalles como el permitir el caso de open a resolved, ya que un usuario podria resolver una alerta sin necesidad de reconocerla, y ya sabe la causa.  

y por ultimo prompt utilice: "Funcion pura compute_statistics(values: list[float]) que devuelva
count/min/max/average. Lista vacia -> todo None excepto count=0.
Redondea average a 2 decimales. TDD: tests primero."  

Aqui no tuve ningun problema con los resultados, porque al ser logica matematica, no tiene muchas complicaciones para la IA al contrario de casos mas subjetivos.  

## Entrada 3: 

Aqui tuve que conectar las cosas hechas anteriormente a FastAPI y SQLALchemy, y agregar varias cosas como el manejo global de errores.  

El primer prompt que use fue "Actualiza AnomalyDetectionService para usar determine_severity del
dominio puro en vez de la logica simple anterior. AlertModel necesita
un campo severity nuevo."  

El codigo que me dio no encontre problemas en su diseño, los problemas empezaron cuando empezaba a interactuar con otros codigos, errores que corregi con ayuda de los tests de mypy y ruff.  

El segundo prompt que use fue: "Conecta AlertStatus (ya creado ayer) a AlertQueryService: agrega
change_status(alert_id, new_status) que valide la transición con
can_transition antes de persistir, y un endpoint PATCH /alerts/{id}."  

La IA me genero codigo que funciona como lo pedi, con el endpoint PATCH devolviendo 409 cuando la transicion es invalidad y 404 si la alerta no existe, aqui no tuve problemas mas que el ruff test que necesitaba cambios.  

El tercer prompt fue "Configura logging en JSON para toda la app (formatter custom), y agrega
un exception_handler global en FastAPI que convierta cualquier excepcion
no controlada en un 500 limpio sin exponer el traceback al cliente."  

Me genero un codigo con el cual no tuve ningun problema, contando con el handler global registrado con @app.exception_handler(Exception).  

Y por ultimo promt que use fue "Agrega GET /metrics que devuelva conteos: sensores activos, total de
lecturas, alertas abiertas. Necesita metodos de conteo nuevos en cada
repositorio."  

Aqui si tuve que cambiar parte del codigo, ya que verifique y vi que me habia cambiado algunas cosas a la version anterior, usando session.query() (1.x) en lugar de select() (2.x), entonces lo tuve que terminar arreglando.  

## Entrada 4:  
En este dia decidi hacer la migracion de Alembic, le pedi a la IA, el prompt" Dame la serie de pasos para poder hacer la migracion a Alembic de mi proyecto"  

La IA me dio una serie de pasos que segui, el problema que me encontre es que no aparecian todas las tablas que deberian, utilice la IA para que me diera posibles soluciones, de las opcciones que me dio la que termine usando y me termino funcionando fue borrar las versiones anteriores de Alembic que tenia de las migraciones pasadas.  

Tambien cuando estaba usando el docker, hice unas pruebas y me di cuenta que no me estaba registrando los threshold, asi que tuve que checar los codigos y me di cuenta que faltaban partes de la cadena de comunicacion, asi que le pedi ayuda a la IA, para que me dijiera como solucionarlo, la cual me dijo que habia que cambiar algunas partes de varios codigos, yo aceptando sus cambios.  



## Entrada 5:  

E





