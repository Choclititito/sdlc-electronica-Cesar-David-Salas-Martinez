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

Como musico quiero presionar el boton de seleccion y que se registre una sola pulsacion, para evitar saltarme algun efecto por accidente debido al rebote fisico del boton  

Story points: 2  

Scenario: Filtrado del rebote

Given el pedal esta encendido
When presiono el boton para el cambio de efecto  
Then el efecto actual cambia al siguiente una sola vez  
And Cualquier señal electrica adicional en los siguientes 50ms es ignorada.

Scenario: Mantener el botón presionado no genera múltiples cambios  

Given el pedal está encendido  
When mantengo presionado el botón de selección de efecto por más de 1 segundo sin soltarlo  
Then el efecto cambia al siguiente disponible exactamente una sola vez  
And no se registran cambios adicionales hasta que el botón sea liberado por completo.  

Scenario: Registrar pulsaciones dobles intencionales rápidas  

Given el pedal está encendido  
When presiono y suelto el botón de selección dos veces intencionalmente en un lapso de 150 milisegundos  
Then el sistema registra ambas pulsaciones como válidas  
And el efecto avanza exactamente dos posiciones en la lista.  

Scenario: Filtrado de rebote al soltar el botón  

Given el pedal está encendido y el botón de selección se encuentra presionado  
When libero el botón físicamente  
Then el sistema ignora cualquier fluctuación eléctrica durante los siguientes 50 milisegundos  
And el efecto actual se mantiene activo sin saltar al siguiente.  

### Critica de la IA :  
¿Es verificable? (Verificabilidad): Alta. La historia utiliza límites de tiempo exactos (50ms, 1s, 150ms) en lugar de aproximaciones. Esto permite que un tester o un script automatizado inyecte señales eléctricas precisas y evalúe los cambios de estado de forma 100% determinista.  
¿Es ambiguo? (Ambigüedad): Nula. Los escenarios describen el comportamiento puramente desde el exterior (caja negra) sin dictar cómo debe programarse el código interno. Además, los eventos (When) y resultados (Then) están perfectamente separados.  
Casos Borde Cubiertos (Edge Cases): Excelente cobertura física. No solo evalúa la pulsación ideal, sino que blinda al sistema contra el ruido al soltar el botón (release bouncing), pulsaciones dejadas presas por error (long press) y pulsaciones múltiples intencionales rápidas.  


# US-02: Entrada de audio y prevención de ruidos   

Como músico, quiero poder conectar y desconectar mi instrumento mediante un cable jack 6.3mm macho sin que se generen picos de ruido en la señal, para evitar sonidos molestos en vivo o dañar los altavoces.  

Story points: 3  

Scenario: Silenciamiento automático al conectar el instrumento (Auto-Mute) Nota: Este comportamiento aplica sin importar si el efecto del pedal está activado o en bypass.  

Given el pedal está encendido y listo para procesar audio  
When se inserta el cable jack 6.3mm en la entrada  
Then la señal de salida del pedal cae a cero de forma inmediata  
And se mantiene completamente silenciada durante los siguientes 100 milisegundos para bloquear el ruido eléctrico de la conexión.  

Scenario: Silenciamiento automático al desconectar el instrumento  

Given el pedal está encendido y la entrada de audio está conectada  
When se extrae físicamente el cable de la entrada  
Then la salida de audio del pedal se silencia de forma inmediata  
And se bloquea cualquier transitorio eléctrico hacia la salida de audio durante la desconexión.  

Scenario: Inserción inusualmente lenta del cable 

Given el pedal está encendido  
When se inserta el cable lentamente, generando un contacto eléctrico inestable por más de 100 milisegundos  
Then el temporizador interno de silenciamiento se reinicia con cada fluctuación detectada  
And la salida de audio solo se reactiva tras registrar 100 milisegundos continuos de conexión física estable.  

Scenario: Conexión y desconexión ultrarrápida (Prevención de bloqueos)  

Given el pedal está encendido y silenciado por una conexión reciente  
When el cable se extrae nuevamente antes de que termine el temporizador de gracia de 100 milisegundos  
Then el sistema cancela el temporizador de reactivación de audio  
And el pedal permanece de forma segura en estado silenciado (Mute) hasta que ocurra una nueva conexión estable.  

Scenario: Conexión de un cable estéreo (TRS) por accidente  

Given el pedal está encendido  
When el usuario inserta un cable estéreo (TRS Tip-Ring-Sleeve) en lugar de un cable mono (TS)  
Then el sistema aplica correctamente el silenciamiento inicial de 100 milisegundos  
And el sistema puentea a tierra la señal del anillo (Ring) para funcionar como una conexión Mono estándar sin generar zumbidos constantes.  

### Critica de la IA:  
¿Es verificable? (Verificabilidad): Alta. La prueba está aislada al dominio del pedal: evalúa que "la señal de salida cae a cero" durante tiempos medibles (100ms), lo cual es comprobable con un osciloscopio sin depender de si un amplificador externo funciona o no.  
¿Es ambiguo? (Ambigüedad): Nula. Establece claramente que esta regla de protección se aplica a nivel de sistema, sin importar si el efecto principal está activado o en bypass.  
Casos Borde Cubiertos (Edge Cases): Muy robustos. Resuelve los principales dolores de cabeza del hardware analógico: ruidos por desconexión, falsos contactos por inserciones lentas, bloqueos del temporizador por cables que entran y salen rápido, y cortocircuitos causados por conectar un cable estéreo (TRS) por accidente.  

# US-03: Latencia imperceptible en el procesamiento de efectos (Efectos sin retraso)  

Como músico, quiero poder tocar mi instrumento sin percibir un retraso entre la nota tocada y el sonido procesado, para mantener la coherencia rítmica en vivo y evitar que el desfase arruine mi interpretación.  

Story points: 5  

Scenario: Latencia máxima bajo procesamiento normal  

Given el pedal está encendido, el efecto activado y el sistema está listo para procesar audio  
When una señal de audio ingresa por el jack de entrada (Input)  
Then el tiempo de tránsito total de la señal desde la entrada física hasta la salida procesada (Output) es estrictamente menor a 5 milisegundos.  

Scenario: Transición de efectos en tiempo real sin picos de latencia  

Given el pedal está procesando audio y manteniendo una latencia menor a 5ms  
When el usuario cambia el algoritmo de efecto pisando el footswitch de selección  
Then la carga del nuevo algoritmo en memoria no interrumpe el flujo de audio  
And el sistema mantiene la latencia estricta menor a 5 milisegundos durante toda la transición.  

Scenario: Prevención de ruidos ante sobrecarga de CPU (Buffer Underrun)  

Given el microcontrolador está ejecutando un algoritmo con alta demanda matemática  
When el tiempo de cálculo excede el límite temporal del bloque actual (riesgo de Buffer Underrun)  
Then el sistema da prioridad a la estabilidad y evita colgarse (Watchdog)  
And descarta de forma segura las muestras rezagadas aplicando un suavizado (interpolación) para evitar emitir chasquidos digitales de alta frecuencia (glitches).  

### Critica de la IA:  
¿Es verificable? (Verificabilidad): Alta. El criterio de aceptación principal define un umbral numérico estricto ("menor a 5 milisegundos") para el tiempo de tránsito desde el pin de entrada hasta el pin de salida, lo cual es la definición técnica exacta y medible de latencia.  
¿Es ambiguo? (Ambigüedad): Nula. La redacción no deja espacio a interpretaciones sobre si la latencia es "molesta" o "lenta" (que serían términos subjetivos); se rige por un límite matemático.  
Casos Borde Cubiertos (Edge Cases): Nivel profesional en firmware. Contempla escenarios de estrés del sistema operativo en tiempo real (RTOS), asegurando que el cambio de efectos al vuelo no genere picos de latencia, y dicta una estrategia de mitigación segura (interpolación) si la CPU no logra terminar sus cálculos a tiempo (Buffer Underrun).  

# US-04: Transiciones limpias sin ruidos (Anti-Pop) al cambiar de efectos  

Como músico, quiero cambiar entre diferentes algoritmos de efectos en tiempo real sin que se generen chasquidos digitales o transitorios eléctricos en la señal, para mantener transiciones acústicas limpias y profesionales durante mi presentación.  

Story points: 5 (Subió de 3 a 5 por la complejidad de procesar el cruce por cero y las colas de audio)  

Scenario: Transición de efecto en el cruce por cero (Zero-Crossing)  

Given el pedal está procesando una señal de audio con el Efecto A activado  
When el usuario presiona físicamente el footswitch para cambiar al Efecto B  
Then el sistema espera al siguiente cruce por cero de la onda de audio (amplitud 0V) para ejecutar el cambio de algoritmo  
And la señal de salida no presenta ningún pico de voltaje abrupto (DC offset) que supere la amplitud de la señal original. 

Scenario: Manejo de colas acústicas (Spillover / Trails) al cambiar de efecto  

Given el pedal está procesando un efecto basado en tiempo (ej. Delay o Reverb)  
When el usuario cambia repentinamente a un efecto de categoría distinta (ej. Distorsión)  
Then el algoritmo de Delay/Reverb se mantiene activo internamente procesando su "cola" de repeticiones de forma paralela  
And el audio de la guitarra se rutea inmediatamente solo al nuevo efecto seleccionado, mezclándose suavemente con la cola del efecto anterior sin cortes abruptos.  

Scenario: Cambios de efecto ultrarrápidos (Button mashing / Estrés)  

Given el pedal está procesando audio de forma normal  
When el usuario presiona el footswitch de cambio de efecto múltiples veces consecutivas en un lapso menor a 50 milisegundos  
Then el sistema registra el último estado seleccionado  
And consolida el cambio en una única transición limpia y segura, evitando sobrecargar la CPU o generar ruido digital (glitches).  

### Critica de la IA:  
¿Es verificable? (Verificabilidad): Alta. Se eliminó la frase subjetiva "no tiene sonido de pop" y se reemplazó por algo concreto. Un ingeniero puede conectar un osciloscopio y validar que el cambio ocurre exactamente donde la onda cruza la línea media.  
¿Es ambiguo? (Ambigüedad): Nula. Se definió claramente el gatillo de la acción y se eliminó la solución técnica impuesta en el borrador original ("se mantiene silenciosa 10ms"), dándole libertad al código DSP para hacer el cruce por cero, que es la solución matemáticamente correcta.  
Casos Borde Cubiertos (Edge Cases): Nivel Senior en procesamiento de señales. Contempla el fenómeno de Spillover (evitando que el cambio de efecto corte las repeticiones de un delay de golpe, lo cual suena muy poco natural), y protege al microcontrolador de saturarse si el músico pisa el botón a toda velocidad tratando de trabar el sistema.

# US-05: Adaptación de impedancia de entrada y preservación del tono (Buffered Bypass)  

Como músico, quiero conectar diferentes tipos de instrumentos (con pastillas pasivas, activas o piezoeléctricas) sin que se degrade la respuesta en frecuencia de mi señal, para mantener el tono original intacto antes de aplicar cualquier efecto.  

Story points: 5  

Scenario: Preservación de respuesta en frecuencia para pastillas de alta impedancia  

Given el pedal está encendido y conectado a la cadena de audio  
When se conecta un instrumento en la entrada física (Input)  
Then el circuito presenta una impedancia de entrada constante de al menos 1 MΩ (Megaohmio)  
And la respuesta en frecuencia de la señal preamplificada se mantiene plana (±1 dB) en el rango de 20 Hz a 20 kHz respecto a la original.  

Scenario: Margen dinámico (Headroom) para pastillas activas o nivel de línea  

Given el pedal está encendido y la etapa de entrada analógica está activa  
When se inyecta una señal de alta amplitud (ej. pastillas activas de 18V o sintetizadores)  
Then la etapa de preamplificación procesa la señal sin aplicar saturación destructiva (clipping analógico)  
And la distorsión armónica total (THD) de la señal acondicionada se mantiene por debajo del 0.1% antes de entrar al convertidor digital (ADC).  

Scenario: Comportamiento del Buffered Bypass ante pérdida de energía  

Given el pedal está en modo "Desactivado" (Bypass) permitiendo el paso de la señal limpia  
When el sistema sufre una desconexión o pérdida total de alimentación eléctrica  
Then la señal de audio se interrumpe de forma segura (comportamiento esperado de un Buffered Bypass activo)  
And no se envían ruidos transitorios no controlados hacia el amplificador.  

### Critica de la IA:  
¿Es verificable? (Verificabilidad): Alta. Se eliminaron por completo las descripciones acústicas subjetivas (como "conservar el brillo") y se reemplazaron por métricas de laboratorio estándar: impedancia > 1 MΩ, respuesta plana ±1 dB, y THD < 0.1%. Un ingeniero electrónico puede conectar un analizador de espectro y validar el requerimiento con números exactos.  
¿Es ambiguo? (Ambigüedad): Nula. Se eliminó el detalle de implementación de hardware (la mención estricta a usar un "preamplificador JFET"), dejando al diseñador de hardware la libertad de usar amplificadores operacionales, JFETs o cualquier otra tecnología, siempre y cuando cumpla con los parámetros matemáticos exigidos. Además, aclara explícitamente que la arquitectura es de tipo "Buffered Bypass".  
Casos Borde Cubiertos (Edge Cases): Nivel Profesional. Contempla el riesgo de saturar la entrada con instrumentos modernos de muy alta salida (pastillas activas) asegurando el headroom. Además, estipula el comportamiento de falla física más importante de un Buffered Bypass: qué pasa con la señal de la guitarra si el pedal se queda repentinamente sin batería en pleno concierto.  

# US-06: Transferencia de datos de audio directa (DMA) sin bloqueo de CPU  

Como arquitecto de firmware, quiero que la transferencia de las muestras de audio desde el hardware a la memoria se realice mediante Acceso Directo a Memoria (DMA), consumiendo menos del 2% del tiempo de procesamiento, para liberar la CPU principal y dedicarla exclusivamente a los cálculos matemáticos de los algoritmos de efectos.  

Story points: 8  

Scenario: Recepción de bloque de audio completo vía I2S (Carga inicial)  

Given el conversor de audio (Codec) está configurado y el controlador DMA está inicializado  
When un bloque continuo de 256 muestras de audio se llena en el periférico de entrada I2S  
Then el controlador DMA transfiere el bloque a la memoria RAM (RX Buffer) sin ejecutar instrucciones de movimiento en la CPU principal  
And el sistema dispara una única interrupción de hardware (Callback RxCplt) solo al finalizar el bloque completo de 256 muestras para iniciar su procesamiento.  

Scenario: Flujo de audio continuo mediante Doble Búfer (Ping-Pong)  

Given el sistema está procesando audio en tiempo real y el DMA acaba de llenar el Búfer A  
When la CPU principal comienza a procesar matemáticamente las muestras del Búfer A  
Then el controlador DMA cambia automáticamente su puntero de escritura hacia el Búfer B (Double Buffering)  
And el hardware continúa capturando la señal del instrumento sin perder ni una sola muestra de audio mientras la CPU trabaja.  

Scenario: Protección y alerta ante sobrecarga matemática (DMA Overrun)  

Given el sistema está utilizando la arquitectura de doble búfer  
When el algoritmo de efectos es demasiado pesado y la CPU no termina de procesar el Búfer A antes de que el DMA termine de llenar el Búfer B  
Then el controlador DMA dispara una interrupción de error por desbordamiento (ErrorCallback / Overrun)  
And el sistema descarta el búfer más antiguo de forma controlada y enciende el LED de estado en color rojo para alertar al desarrollador sobre la sobrecarga de la CPU.  

### Crtica de la IA:  
¿Es verificable? (Verificabilidad): Alta. Se cambió la petición vaga de "no ralentizar la CPU" por un criterio de aceptación cuantitativo ("menos del 2% del tiempo de procesamiento"). Esto permite a un ingeniero usar un profiler de hardware o pines de depuración para medir los ciclos de reloj exactos que toma la transferencia y validar que se cumple la métrica.  
¿Es ambiguo? (Ambigüedad): Nula. Los escenarios describen con precisión quirúrgica qué periféricos interactúan (I2S, DMA, CPU, Memoria RAM) y dictan exactamente cuándo deben dispararse las interrupciones de Callback.  
Casos Borde Cubiertos (Edge Cases): Nivel Arquitecto de Firmware. Se incluyó la mecánica de Ping-Pong (doble búfer), que es el único método físico para no perder audio mientras el microcontrolador hace matemáticas. Además, se cubrió el peor escenario posible (DMA Overrun): definiendo exactamente cómo debe comportarse el hardware si el código de un programador satura la CPU y choca con la entrada de datos en tiempo real.  

#  US-07: Control suave y preciso de la ganancia (Perilla moduladora)  

Como músico, quiero controlar la ganancia de salida del efecto usando una perilla física, para poder ajustar mi volumen en el escenario de forma precisa y sin introducir ruidos digitales en la señal.  

Story points: 5  

Scenario: Silenciar el efecto al límite antihorario  

Given el pedal está encendido y el efecto está activado  
When giro la perilla de ganancia al límite máximo antihorario (0%)  
Then el algoritmo silencia completamente la señal procesada (-infinito dB).  

Scenario: Máxima ganancia permitida al límite horario  

Given el pedal está encendido y el efecto está activado  
When giro la perilla de ganancia al límite máximo horario (100%)  
Then la señal procesada aplica un realce de ganancia exacto de +12 dB.  

Scenario: Prevención de ruido digital (Zipper Noise) e inestabilidad (Jitter)  

Given el pedal está procesando audio y leyendo el convertidor analógico-digital (ADC)  
When el usuario gira la perilla rápidamente o la suelta en una posición intermedia  
Then el código aplica una interpolación matemática para suavizar la transición de volumen  
And filtra las fluctuaciones eléctricas (Jitter) del potenciómetro para evitar el "ruido de cremallera" en los altavoces.  

Scenario: Transparencia total con el pedal desactivado (Bypass)  

Given el pedal está encendido pero el efecto está desactivado (Bypass)  
When la perilla de ganancia se mueve en cualquier sentido o velocidad  
Then la amplitud de la señal de salida no se ve alterada (ganancia unitaria de 0 dB respecto a la entrada).  

### Critica de la IA:  
¿Es verificable? (Verificabilidad): Alta. Se corrigió el término abstracto de "salida máxima" y se reemplazó por valores acústicos exactos ("-infinito dB" y "+12 dB"). Ahora un programador sabe exactamente qué límites matemáticos poner en su código y un tester puede medir la amplitud resultante.  
¿Es ambiguo? (Ambigüedad): Nula. Se corrigió la sintaxis de Gherkin que estaba rota. Ahora las condiciones previas están estrictamente en el Given, la acción física del usuario está en el When, y el resultado esperado del sistema está aislado en el Then.  
Casos Borde Cubiertos (Edge Cases): Nivel Arquitectura de Hardware. Se integró un escenario indispensable para leer potenciómetros físicos: obligar al programador a lidiar con el Jitter del ADC y suavizar los saltos de volumen (Zipper noise). Sin este escenario, un simple control de volumen arruinaría la experiencia del músico con chasquidos constantes.  

# US-08: Prevención de desbordamiento y saturación digital (Limitador / Hard-Clipping)  

Como arquitecto de firmware, quiero implementar un límite de saturación matemática estricto en la etapa final de salida, para proteger al convertidor digital-analógico (DAC) de valores fuera de rango y evitar ruidos destructivos por desbordamiento numérico.  

Story points: 5  

Scenario: Saturación matemática en el pico positivo (Límite superior)  

Given el sistema DSP está procesando bloques de audio y calculando la ganancia final  
When el algoritmo produce una amplitud que excede el límite digital máximo seguro (ej. superior a +1.0 en punto flotante)  
Then el sistema aplica una lógica de saturación (Hard-Clipping) anclando el valor de salida exactamente en +1.0  
And el convertidor DAC procesa el tope máximo sin generar errores de lectura.  

Scenario: Saturación matemática en el valle negativo (Límite inferior asimétrico)  

Given el sistema DSP está procesando las oscilaciones negativas de la onda de audio  
When el cálculo matemático genera un valor por debajo del límite mínimo permitido (ej. inferior a -1.0 en punto flotante)  
Then el algoritmo iguala el valor exactamente a -1.0  
And previene que el software intente enviar voltajes negativos inválidos al hardware del DAC.  

Scenario: Prevención de desbordamiento cíclico (Integer Wrap-around) con alta eficiencia  

Given la conversión final de la señal a números enteros de 16 bits (rango -32768 a 32767) para el envío físico al hardware  
When una suma de señales o ecualización extrema sobrepasa el valor entero 32767  
Then el código ancla la variable a 32767 en lugar de permitir que dé la vuelta cíclicamente a -32768  
And el sistema utiliza instrucciones de saturación intrínsecas del microcontrolador (DSP hardware instructions) en lugar de bloques condicionales if/else para no castigar el tiempo de la CPU.  

### Critica de la IA:  
¿Es verificable? (Verificabilidad): Alta. Ahora se establecen límites numéricos exactos (+1.0, -1.0, 32767, -32768) que un programador puede usar inmediatamente para escribir Unit Tests basados en assert().  
¿Es ambiguo? (Ambigüedad): Nula. La acción de "recortar" se reemplazó por el término técnico correcto: Saturación matemática / anclaje. Esto le dice al desarrollador que los valores excedentes no se descartan ni rebotan (foldback), sino que se igualan al tope máximo.  
Casos Borde Cubiertos (Edge Cases): Nivel Senior en Procesamiento de Señales (DSP). Se integraron tres salvavidas críticos: la protección asimétrica (evaluando los valles negativos de la onda, no solo los picos), la prevención del catastrófico Integer Wrap-around (que acústicamente suena como un disparo en los monitores), y el uso de operaciones de hardware para no consumir los ciclos del procesador.  

# US-09: Verdadero Bypass (True Bypass) Electromecánico y Modo Seguro  

Como músico, quiero que al desactivar el efecto la señal de mi instrumento pase directamente de la entrada a la salida sin tocar ningún circuito activo o convertidor digital, para mantener mi tono original intacto y asegurar que el audio siga fluyendo incluso si el pedal se queda sin batería.  

Story points: 3  

Scenario: Continuidad total sin energía (True Bypass físico)  

Given el pedal no tiene ninguna fuente de alimentación eléctrica conectada (sin batería o desconectado de la red)  
When el usuario inyecta señal de audio a través del jack de entrada (Input)  
Then existe continuidad eléctrica física (resistencia cercana a 0 Ω) directamente hacia el jack de salida (Output)  
And la señal fluye con una latencia de procesamiento de exactamente 0 milisegundos, sin pasar por el microcontrolador.  

Scenario: Transición silenciosa hacia el bypass (Prevención de Pop mecánico)  

Given el pedal está encendido y el efecto está activado  
When el usuario presiona el footswitch para desactivar el efecto (cambio a Bypass)  
Then el relé mecánico conmuta puenteando la entrada con la salida  
And las resistencias de pull-down del circuito descargan cualquier voltaje continuo (DC offset) acumulado en los capacitores, previniendo que suene un "pop" fuerte en el amplificador al hacer el cambio físico.  

Scenario: Recuperación automática ante falla de alimentación (Fail-Safe)  

Given el pedal está encendido y procesando audio activamente  
When ocurre una pérdida repentina de energía (batería agotada o desconexión del eliminador)  
Then el relé de conmutación de estado sólido pierde su voltaje de retención y cae a su estado "Normalmente Cerrado" (NC)  
And el sistema puentea automáticamente la entrada con la salida, asegurando que la guitarra no se quede silenciada en medio de una presentación.  

### Critica de la IA:  
¿Es verificable? (Verificabilidad): Alta. Se tienen métricas 100% testeables por un ingeniero de control de calidad (QA): medir con un multímetro que la resistencia entre entrada y salida sea de ~0 Ω, y comprobar con un osciloscopio que la latencia sea de 0ms.  
¿Es ambiguo? (Ambigüedad): Nula. Se eliminó la gran contradicción del borrador original que pedía Given el pedal está encendido para probar el bypass. Ahora queda explícitamente claro que un verdadero True Bypass es un puente mecánico que debe funcionar independiente del estado lógico o eléctrico del sistema.  
Casos Borde Cubiertos (Edge Cases): Nivel Diseño de Hardware. Se integraron dos escenarios vitales en el diseño de circuitos analógicos: la protección contra el "pop" mecánico al pisar el interruptor (usando resistencias pull-down), y el comportamiento Fail-Safe, garantizando que si el equipo muere a mitad de un concierto, el relé cae a una posición segura que deja pasar el sonido de la guitarra intacto.  

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


























