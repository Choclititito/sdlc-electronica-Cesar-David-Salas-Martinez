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
def celsius_to_fahrenheit(c: float) -> float:
    """Convert a Celsius temperature to Fahrenheit rounded to 2 decimals.

    Args:
        c: Temperature in degrees Celsius.

    Returns:
        Temperature in degrees Fahrenheit rounded to 2 decimal places.
    """
    return round(c * 9.0 / 5.0 + 32.0, 2)

Abajo poniendo un comentario diciendo: #creado por aider con la API de Gemini, esto para dar el siguiente promt " Crea debajo del comentario "#creado por aider con la API de Gemini" escribe una funcion pura celsius_to_farenheit(c:float) -> float con type hints completos, docstring, sin dependencias externas, redondeo a 2 decimales"  
Todo esto para poder tener una comparativa directa entre los 2, lo malo es que lo que termino haciendo fue solamente cambiar el comentario y reescribir todo el codigo, aunque termino quedando igual, como se puede ver en el archivo.  

¿En que supera a Copilot?:  
Siento que es mejor en el hecho de poder funcionar con diferentes inteligencias artificiales, haciendo que su uso no se vea limitado solamente a una.  

¿En que falla?:  
Pues a mi me fallo en lo que le pedi, interpreto mal una instruccion que a mi parecer era bastante sencilla, y no debio haber tenido que fallar, ademas que es mas incomod de usar que el copilot que ya tiene una integracion directamente en el VSC.  





## Dia 3  

## Dia 4  

## Dia 5  





