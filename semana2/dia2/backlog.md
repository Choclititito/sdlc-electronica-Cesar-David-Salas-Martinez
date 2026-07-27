#BACKLOG


# Objetivo del producto: Aplicar efecto a una señal de audio  

Como guitarrista,quiero que el ESP32 aplique un efecto de audio a seleccion entre Distorsion, Chorus, Delay, para obtener un sonido diferente a seleccion mia.  

Criterios de Aceptación:  

Scenario: Seleccionar efecto  

Given el pedal está encendido  
When presiono el boton para seleccionar el efecto  
Then uno de los  3 LEDs indicadores de efecto se enciende dependiendo del efecto seleccionado  
And la señal de salida se procesa con el algoritmo que es seleccionado  

Scenario: Activar el efecto con exito  

Given el pedal está encendido y conectado a la guitarra y al amplificador  
When presiono el interruptor (footswitch) para activar el pedal  
Then el LED indicador se enciende  
And la señal de salida se procesa con el algoritmo que se selecciono sin un retraso (latencia) perceptible.  

Scenario: Modo Bypass (efecto apagado)  

Given el pedal está encendido pero el efecto está desactivado  
When toco las cuerdas de la guitarra  
Then la señal de audio pasa limpia (bypass) hacia el amplificador sin alteraciones  
And el LED indicador permanece apagado.  

### Critica de la IA:  
El material refleja un curso diseñado no solo para enseñarte a programar, sino para formarte como un ingeniero de software completo, capaz de gestionar un producto desde su concepción y planificación, hasta su arquitectura técnica y despliegue final con estándares de la industria.  

# US-01: Evitar "bouncing" de los botones

Como desarrollador quiero evitar el presionar un boton y que este detecte varias pulsaciones, para evitar un cambio de efecto no deseado.  

Story points: 2  

Scenario: Se presiona el boton de seleccion  

Given el pedal esta encendido
When presiono el boton para el cambio de efecto  
Then un algoritmo detecta la primera pulsacion y el "Bouncing" lo ignora durante 20 a 100 milisegundos.

### Critica de la IA :  
Verificabilidad: Débil. Usar un rango de tiempo (20 a 100ms) hace que la prueba no sea determinista. Se debe usar un valor límite específico.  
Ambigüedad: Alta. La historia describe detalles de implementación ("un algoritmo") en lugar del comportamiento del sistema (caja negra), y está redactada desde la perspectiva del desarrollador en lugar del usuario final.  
Casos Borde Faltantes: No define el comportamiento ante pulsaciones prolongadas (long press), botones atascados o pulsaciones intencionales consecutivas muy rápidas.  

# US-02: Entrada de audio  

Como musico quiero poder conectar mi instrumento mediante un cable jack 6.3mm macho sin que suene un "pop" en el amplificador, para evitar ruidos molestos cuando se conecta  

Story points: 3  

Scenario: Se conecta el cable al pedal activo  

Given el pedal esta encendido, activado con el footswicht, conectado al amplificador  
When se conecta el cable jack 6.3mm  
Then no se escucha ningun sonido en el amplificador  
And cualquier señal dde ruido electrico de la conexion se ignora durante 100 milisegundos y es ignorada  

Scenario: Se conecta el cable al pedal desactivado  

Given el pedal esta encendido, desactivado con el footswicht, conectado al amplificador  
When se conecta el cable jack 6.3mm  
Then no se escucha ningun sonido en el amplificador  
And cualquier señal dde ruido electrico de la conexion se ignora durante 100 milisegundos y es ignorada  

### Critica de la IA:  
Verificabilidad: Media. Evaluar el sonido "en el amplificador" no es verificable directamente por el sistema; se debe medir que la señal de salida del propio pedal sea nula (cero transitorios eléctricos).  

Ambigüedad: Baja, pero hay redundancia en la redacción ("se ignora... y es ignorada") y los dos escenarios descritos podrían fusionarse en uno solo, ya que el comportamiento esperado es idéntico sin importar el estado del footswitch.  

Casos Borde Faltantes: No cubre el ruido de desconexión (que genera el mismo problema), inserciones de cable inusualmente lentas que duren más del tiempo de gracia de 100ms, ni el uso de cables incorrectos (estéreo).  

# US-03: Efectos sin retraso  

Como musico quiero poder tocar sin sentir un retraso entre lo que toco y lo que se escucha en el amplificador, esto para evitar una incoherencia entre lo que se toca y lo que suena.   

Story points: 5  

Scenario: Se esta tocando el instrumento  
Given el pedal esta encendido, activdado, y conectado al amplificador  
When se empieza a tocar el instrumento  
Then la salida del audio procesa el audio en un tiempo menor a 5 milisegundos, y la salida manda la señal procesada  

### Critica de la IA:  
Verificabilidad: Excelente. El umbral de 5ms es un valor cuantitativo que se puede medir fácilmente con equipo de laboratorio (osciloscopio).  

Ambigüedad: Baja, pero la redacción del Then confunde la etapa de salida física con la etapa de procesamiento interno.  

Casos Borde Faltantes: No especifica el comportamiento de falla si el algoritmo exige demasiada carga a la CPU y no logra entregar la muestra a tiempo (buffer underrun), ni garantiza este tiempo durante transiciones de cambio de efecto.  

# US-04: Evitar sonidos de "pop" al intercambiar de efecto.  

Como musico quiero poder evitar un sonido de "pop" cuando intercambio los efectos sin desactivar el pedal, para asi hacer transiciones mas limpias.  

Story points: 3  

Scenario: Intercambio el efecto con el boton  
Given el pedal esta encendido, activado y conectado a un amplificador  
When se empiezan a cambiar de efectos  
Then la señal de salida no tiene esa señal de "pop"  
And se mantiene silenciosa 10ms  

### Critica de la IA:  
Verificabilidad: Media. Los 10ms son medibles, pero "no tener pop" no es un criterio de ingeniería cuantificable (se debe hablar de picos de voltaje o transitorios).  

Ambigüedad: El momento exacto de la acción ("se empiezan a cambiar") no define si el disparador es al presionar o soltar el botón. Además, estipula una solución técnica (silencio de 10ms) en lugar de un comportamiento funcional.  

Casos Borde Faltantes: Cortar la señal bruscamente para silenciarla puede generar el mismo pop que intentas evitar si no se hace en un "cruce por cero" (zero-crossing). Tampoco define qué ocurre con las colas de efectos como el delay o la reverb al hacer el cambio.  

# US-05: Adaptacion de impedancia de entrada  

Como musico quiero que se puedan usar diferentes tipos de pastillas con el pedal, haciendo que el pedal respete el tono original de estas.  

Story points: 5  

Scenario: Se conecta un instrumento con pastillas piezoelectricas, con el efecto encendido.  

Given el pedal esta encendido, activado y conectado a un amplificador  
When se conecta y toca el instrumento  
Then la señal de entrada conserva los tonos y brillo original de la guitarra antes de pasarla por el efecto  
And la señal es preamplificada con un preamplificador JFET  

Scenario: Se conecta un instrumento con pastillas piezoelectricas, con el efecto apagado.  

Given el pedal esta encendido, desactivado y conectado a un amplificador  
When se conecta y toca el instrumento  
Then la señal de entrada conserva los tonos y brillo original de la guitarra, para salir de esta misma manera en la salida 
And la señal es preamplificada con un preamplificador JFET  

### Critica de la IA:  
Verificabilidad: Muy baja. "Conservar el brillo y tono" es subjetivo. Se debe especificar un requerimiento técnico como "mantener una impedancia de entrada > 1 MΩ" o "respuesta en frecuencia plana".  

Ambigüedad: Alta. El Gherkin dicta cómo se debe construir el hardware (usando un JFET) en lugar de describir el comportamiento esperado. Además, la historia habla de "varias pastillas" pero solo prueba una.  

Casos Borde Faltantes: No contempla qué sucede si se inyecta una señal de nivel de línea o de pastillas activas de alto voltaje que sature la etapa analógica. Tampoco define el comportamiento si el pedal pierde energía estando apagado (diferencia entre True Bypass y Buffered Bypass).  

# US-06: Transferencia de datos directa  

Como arquitecto de firmware, quiero que la entrada de datos no relentice al CPU, para tener el CPU totalmente para los algoritmos de efectos  

Story points: 8  

Scenario: Recepción de bloque de audio completo vía I2S.  

Given el conversor de audio (Codec) está configurado y el controlador DMA está inicializado  
When un bloque continuo de 256 muestras de audio se llena en el periférico I2S  
Then el controlador DMA transfiere el bloque a la memoria (RX Buffer) sin ejecutar instrucciones de movimiento en la CPU principal  
And se dispara una única interrupción (Callback RxCplt) al finalizar el bloque de 256 muestras para iniciar el procesamiento.   

### Crtica de la IA:  
Verificabilidad: Excelente. Se puede comprobar en un entorno de desarrollo usando contadores de ciclos de CPU y breakpoints en las interrupciones de hardware.  

Ambigüedad: Muy baja en el escenario. Solo la narrativa superior podría beneficiarse de usar una métrica técnica en lugar de la palabra "ralentice".  

Casos Borde Faltantes: Carece del manejo de doble búfer (Ping-Pong) esencial para no perder audio mientras la CPU procesa el bloque anterior. Tampoco define cómo debe comportarse el hardware si el procesamiento toma más tiempo que la captura de datos (error de desbordamiento).  

#  US-07: Perilla moduladora de la ganancia del pedal  

Como musico, quiero poder controlar la ganancia que me proporciona el pedal, esto para poder controlar el volumen de la salida  

Story points: 3  

Scenario: Se mueve la perrilla en sentido anti horario, hasta que no permita mas vueltas  

Given la perilla esta en una posicion neutra, el pedal esta encendido  
When la perilla llegue al limite, si el pedal esta activo, no habra salida de sonido  

Scenario: Se mueve la perrilla en sentido horario, hasta que no permita mas vueltas  
Given la perilla esta en una posicion neutra, el pedal esta encendido  
When la perilla llegue al limite, si el pedal esta activo, la salida del sonido del pedal sera la maxima  

Scenario: Se mueve la perrilla en cualquier sentido, con el pedal desactivado  
Given la perilla esta en una posicion neutra, el pedal esta encendido  
When la perilla se mueve en cualquier sentido, no se vera afectada la salida de audio  

### Critica de la IA:  
Verificabilidad: Media. "Silencio" es medible, pero "salida máxima" no especifica un valor objetivo en decibelios (dB) o factor de multiplicación, dejando al programador adivinando el límite.  

Ambigüedad: Alta por fallos de formato. Las condiciones del sistema (Given), las acciones (When) y los resultados (Then) están mezclados en la misma oración, rompiendo la estructura lógica de las pruebas.  

Casos Borde Faltantes: Carece de estrategias para lidiar con las limitaciones del hardware: el ruido de lectura estática del potenciómetro (Jitter del ADC) y los chasquidos digitales al cambiar el volumen rápidamente (Zipper noise). No define el comportamiento en posiciones intermedias.  

# US-08: Parada virtual de ganancia  

Como arquitecto de fimware, quiero que haya un limite virtual para la ganancia, asi a pesar de que el programa quiera sacar una ganancia mas alta de lo que puede el microcontrolador, este la limita  

Story points: 5  

Scenario: La señal pasada por el algoritmo del efecto, excede los limites de la salida del microcontrolador  

Given el microcontrolador esta iniciado  
When una señal se genera con un valor mas alto del valido  
Then se recorta la señal de salida para evitar una salida no valida  

### Critica de la IA:  
Verificabilidad: Baja. Se necesitan valores de límite duros y explícitos (ej. > 1.0, > 32767, o > 4095) para poder escribir pruebas de código exactas.  

Ambigüedad: Media. "Recortar" no especifica la técnica matemática (saturación). "Valor válido" no distingue si se está protegiendo el límite de la variable de software o el límite físico del hardware (DAC).  

Casos Borde Faltantes: No contempla la protección contra los límites negativos de la onda, ni protege explícitamente contra el destructivo desbordamiento cíclico de variables en C/C++ (Integer Wrap-around).  

# US-09: Verdadero bypass  

Como musico, cuando el pedal este desactivado quiero que el sonido pase directamente sin pasar por la logica del microprocesador, esto para poder tener el sonido original del instrumento  

Story points: 2  

Scenario: Se toca el instrumento  

Given el pedal esta encendido, esta desactivdado, y el instrumento conectado  
When la señal de la guitarra entra  
Then pasa directamente a la salida  

### Critica de la IA:  
Verificabilidad: Media. Faltan métricas exactas como "latencia de 0ms" o "continuidad física entre los conectores" para asegurar que la señal no entró al convertidor digital (ADC).  

Ambigüedad: Alta. Exigir que el pedal esté "encendido" para que funcione el True Bypass contradice el propósito principal de esta arquitectura (que debe funcionar incluso sin energía).  

Casos Borde Faltantes: No contempla qué ocurre si el pedal pierde alimentación eléctrica (debería puentear la señal automáticamente) ni protege contra el ruido de "pop" mecánico al presionar el switch o relé que une directamente la entrada con la salida.  

# US-10: Recuperación automática del sistema (Watchdog)  

Como músico en vivo, quiero que el pedal se reinicie automáticamente de forma segura si el software interno se congela, para evitar que el sonido se interrumpa o se quede emitiendo un ruido digital continuo durante una presentación.  

Story points: 5  

Scenario: El hilo principal de audio se congela por un error matemático.  
Given el pedal está encendido, el efecto está activado, y el hardware Watchdog Timer está configurado a 500 milisegundos  
When una falla lógica causa un bucle infinito que impide "alimentar" (resetear) el contador del Watchdog  
Then el microcontrolador fuerza un reinicio por hardware al expirar los 500ms  
And un relé mecánico de derivación (Bypass) se cierra automáticamente por falta de voltaje, dejando pasar la señal limpia del instrumento mientras el sistema arranca.  

Scenario: Recuperación de estado tras un reinicio forzado.  
Given el microcontrolador acaba de sufrir un reinicio por el Watchdog Timer  
When el sistema operativo de tiempo real (RTOS) vuelve a iniciar  
Then el pedal arranca en modo "Desactivado" (Bypass) por defecto para no introducir ruido inesperado  
And el LED indicador parpadea en rojo tres veces para notificar al usuario que ocurrió una recuperación de emergencia. 

### Critica de la IA:  
Verificabilidad: Alta. Inyectar fallos (while(1)) para comprobar reinicios en 500ms es una prueba unitaria y de estrés estándar.  

Ambigüedad: Baja. Las precondiciones y los resultados esperados (parpadeo de LED, estado de Bypass seguro) son claros y deterministas.  

Casos Borde Faltantes: No establece protección contra "Boot Loops" si la causa del congelamiento ocurre durante la secuencia de inicio, lo que mantendría el pedal reiniciándose para siempre.  


























