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




