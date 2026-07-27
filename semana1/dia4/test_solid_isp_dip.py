from solid_isp_dip import (
    Calibratable,
    DataProcessor,
    InMemoryRepository,
    Readable,
    Resettable,
    SensorReading,
    Writable,
)  #Importamos todas las clases a probar

# ==========================================
# Tests para DIP (Inversión de Dependencias)
# ==========================================

def test_in_memory_repository_guarda_y_recupera_datos():
    # 1. Preparación y Aislamiento
    repo = InMemoryRepository()
    lectura = SensorReading(sensor_id="TEMP-01", value=23.5) # Se crea un sensor basico
    
    # 2. Ejecución
    repo.save(lectura) #Se guarda la informacion del sensor
    resultado = repo.get_latest("TEMP-01")
    
    # 3. Aserción
    assert resultado is not None
    assert resultado.value == 23.5 #Se verifica si se guardaron los datos
    assert resultado.sensor_id == "TEMP-01"

def test_data_processor_utiliza_el_repositorio_inyectado():
    # 1. Preparación y Aislamiento
    repo_prueba = InMemoryRepository() # Usamos memoria para no tocar la BD real
    procesador = DataProcessor(repository=repo_prueba) # ¡Inyección de dependencias!
    
    # 2. Ejecución
    procesador.process_reading(sensor_id="HUM-99", value=88.0)
    
    # 3. Aserción
    # Verificamos que el procesador realmente delegó el trabajo al repositorio
    dato_guardado = repo_prueba.get_latest("HUM-99") #
    assert dato_guardado is not None
    assert dato_guardado.value == 88.0 #Se confirma el dato

# ==========================================
# Tests para ISP (Segregación de Interfaz)
# ==========================================

# Como no podemos instanciar 'Readable' directamente, creamos un sensor 
# "Falso" (Mock/Dummy) específico para la prueba que respete ese contrato.

class SensorTemperaturaBasico:
    """Implementación concreta que solo adopta el contrato Readable"""
    def read(self) -> float:
        return 42.0  #Se crea un sensor que solamente se puede leer

def test_sensor_concreto_cumple_contrato_readable():
    # 1. Preparación y Aislamiento
    # Le indicamos a Python que este sensor debe ser tratado como 'Readable'
    sensor: Readable = SensorTemperaturaBasico()
    
    # 2. Ejecución
    valor = sensor.read()
    
    # 3. Aserción
    assert valor == 42.0 #Se termina de leer el sensor 

class SensorTemperaturaComplejo:
    """Implementación que usa todas las diferentes funciones"""
    def read(self) -> float:
        return 50.0  #Valor para leer
    
    def write(self, value: 1.0) -> str:
        return "Datos" 
    
    def calibrate(self) -> float:
        return 2.0
    
    def reset(self) -> bool:
        return True

def test_sensor_complejo():
    # Ponemos todas las variables que maneja el sensor complejo
    read : Readable = SensorTemperaturaComplejo()
    write : Writable = SensorTemperaturaComplejo()
    calibrate : Calibratable = SensorTemperaturaComplejo()
    reset : Resettable = SensorTemperaturaComplejo()

    # Ejecutamos las funciones y verificamos que todas cumplan con su contrato
    lecturaTest = read.read()
    escrituraTest = write.write(1.0)
    calibracionTest = calibrate.calibrate()
    reinicioTest = reset.reset()

    # Verificamos los datos
    assert lecturaTest == 50.0
    assert escrituraTest == "Datos"
    assert calibracionTest == 2.0
    assert reinicioTest is True
