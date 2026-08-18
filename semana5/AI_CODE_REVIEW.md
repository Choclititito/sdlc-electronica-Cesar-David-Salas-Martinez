# AI Code Review — ReadingService  

## Herramienta usada  
Aider con gemini/gemini-3.5-flash  

## Hallazgos y decisión  

### 1. Validación de cero absoluto ignoraba la unidad (bug real)  
**Línea**: `_validate_absolute_zero` (antes de la corrección)  
**Problema**: comparaba el valor contra -273.15 sin importar si la unidad era C, F, o K.  
**Decisión**: ACEPTADO. Se corrigió con diccionario ABSOLUTE_ZERO_BY_UNIT.  

### 2. Sin límite máximo en history() (riesgo de rendimiento)  
**Línea**: parámetro `limit` en `history()`  
**Problema**: un cliente podría pedir un limit arbitrariamente grande.  
**Decisión**: ACEPTADO PARCIALMENTE. Ya existía protección a nivel de router
(Query(50, ge=1, le=200)), pero se acepta la defensa adicional en el servicio
como buena práctica de "defensa en profundidad".  

### 3. update_partial validaba con unidad incorrecta cuando no se provee unit  
**Línea**: `update_partial`  
**Problema**: al hacer PATCH solo con value, no se sabía la unidad real de la
lectura existente para validar correctamente.  
**Decisión**: ACEPTADO. Corrección con costo aceptado: una query adicional
(self.get) para obtener la unidad cuando no viene en el patch.  

## Casos borde identificados por Aider  

### 1. Cero absoluto aplicado a unidades no-temperatura  
**Problema**: una lectura de humedad (%) con valor -5 pasaba la validación
porque -5 > -273.15 (el límite de Celsius se usaba como fallback universal).  
**Decisión**: ACEPTADO. Ahora solo se valida cero absoluto si la unidad es
explícitamente C, F, o K.  

### 2. offset negativo sin validar en history()  
**Problema**: un offset negativo viajaba sin control hasta el repositorio,
con riesgo de error de base de datos.  
**Decisión**: ACEPTADO. Se normaliza/valida antes de pasar al repositorio.  

### 3. unit nulo o vacío causando AttributeError  
**Problema**: unit.upper() sobre None truena en record_for_sensor.  
**Decisión**: ACEPTADO. Manejo seguro cuando unit es None.  

## Nota técnica sobre el proceso  
Durante la generación de este fix, el servidor de Gemini devolvió un error
503 (alta demanda) a mitad de la respuesta. Se verificó manualmente que el
archivo resultante fuera sintácticamente válido (import exitoso) y que la
suite de tests completa siguiera pasando (30 passed) antes de aceptar el
commit automático de Aider.  

## Tests agregados (6, cumple el minimo de 5 requerido)  
1. test_record_fahrenheit_below_celsius_limit_but_above_fahrenheit_limit_is_valid  
2. test_record_humidity_negative_value_does_not_raise_absolute_zero_error  
3. test_record_with_none_unit_does_not_raise  
4. test_history_with_negative_limit_raises_value_error  
5. test_history_with_negative_offset_raises_value_error  
6. test_update_partial_without_unit_validates_against_existing_reading_unit  