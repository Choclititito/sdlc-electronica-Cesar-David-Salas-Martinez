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

