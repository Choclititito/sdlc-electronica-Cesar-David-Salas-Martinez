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



