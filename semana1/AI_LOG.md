# BITACORA IA  

##  Entrada Dia 1  
En este dia le di a la IA el siguiente prompt " Explicame varias funciones puras sobre reading con type hints completos, explicame como funcionan cada una de estas y mas informacion cobre las funciones puras Reading, aqui esta el codigo en el que te basaras:"  

adjuntando el codigo del ejercicio, me dio 4 ejemplos de los cuales use 3 y rechace 1.  

-1. Función pura de validación  : Esta la acepte ya que me parecia buen ejemplo para ver como recibir un valor boleano.  

-2 Función pura de transformación (Retorna un NUEVO objeto): Tambien la acepte, ya que me parecio bueno el saber como
hacer un cambio en el valor que te arroja dependiendo el tipo.  

-3 Funcion pura de formateo para humanos: La acepte por que me parecia algo util que se podria usar realmente.  

-4 Funcion pura de agregacion/calculo: La rechace ya que no entendia bien el uso de las listas en este codigo.  

## Entrada dia 2  
En este ejercicio, el prompt fue "Con el codigo que te acabo de pasar, haz estos 4 tests estado inicial, transición RED→GREEN, ciclo completo que vuelve a RED, y conteo de ciclos.", el codigo ya se lo habia dado para pedir
que me explicara algunos puntos que no entendia.  
La IA me dio los 4 test, de los cuales acepte los 2 sin muchos cambios y 2 donde tuve que agregar verificaciones extras que sentia que le hacian falta.  

-1 test_ciclo_completo_vuelve_a_red(): Aqui agregue mas verificaciones despues de cada transicion.  

-2 test_conteo_de_ciclos(): Aqui igualmente agregue verificacion de el numero del conteo despues de cada transicion.  

## Entrada dia 3  
Use este prompt: "Basandote en el siguiente codigo, dame un ejemplo correcto y uno incorrecto de los 3 primero principios SOLID" adjuntando el codigo de ejemplo  

Me dio los 6 ejemplos de los cuales use 4 y 2 los use de base.  

- SmartSensor: cambie los datos que mandaba la función, para poder hacer los test mas fácilmente.

- TemperatureSensor: Este tenia un mismo nombre otra de las clases y daba error.

Después le mande el prompt: "Haz 2 testeos para cada ejemplo correcto de los principios"  

De los 6 test, acepte 4, modifique 1 y rechace 1.  

-def test_humidity_sensor_respeta_firma_liskov: Aquí tuve que arreglar unos nombres de clases que tenia mal por los errores corregidos anteriormente.  

-def test_sensor_reader_retorna_tipo_correcto(): Este lo rechace por ser muy similar al test que esta junto a el.  

## Entrada dia 4  
Use el prompt: "Completa la biblioteca en el siguiente codigo ISP: divide una interfaz gorda (read/write/calibrate/reset) en Readable, Writable, Calibratable. DIP: usa Protocol para que DataProcessor dependa de una abstracción DataRepository:" adjuntando el codigo del PDF.  

Me proporciono un codigo que me tuve que modificar para poder hacer un mejor testeo, agregando en su mayoria salidas de datos especificas (bool, str, float).  

Luego use un prompt para que me ayudara a terminar mis tests: "Hice estos cambios en el codigo, que test me podrian ayudar, aparte de los siguientes" con el codigo modificado y algunos test.  

Me ayudo para poder corregir algunos de mis test que tenian problemas de como trabajar con las clases de Protocol, ademas de sumar algunos.  

Le modifique algunos test, ademas de agregar el de test_sensor_complejo.  

## Entrada dia 5  
Use el prompt: "Necesito resolver esta situacion tienes un driver UART en C estilo embebido: buffers globales, parsing de dos protocolos en funciones sueltas, logging mezclado con comunicación, imposible de testear en aislamiento e imposible de instanciar dos veces. Tu misión: reimplementarlo en Python moderno con SOLID Este cuenta con varias partes:(Las partes especificadas en la actividad), ademas necesito que me des test para cada una de las partes"  

Lo que me dio la IA fue una buena estructura base, donde tuve que hacer algunos cambios para su mejor funcionamiento:  

-Cambiar la forma de importar las demas modulos, ya que habia problemas por la formar en la que lo habia guardado.  

-Reescribir algunos de los test, ya que no los comprendia del todo, intentando simplificarlos y entenderlos con la ia de copilot.  

-Usar la IA de copilot para cambiar algunas funciones y ver que soluciones distintas me daba.  

El uso de la IA de copilot dentro del programa se sintio raro dentro de lo que cabe, por como aveces pensaba soluciones diferentes a lo que yo tenia en mente, pero fue de ayuda para darme una idea de por donde podria ir mi codigo, aunque aveces sentia que se complicaba mas de lo necesario.  





