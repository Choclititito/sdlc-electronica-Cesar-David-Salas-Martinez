from typing import Protocol
from dataclasses import dataclass

# Estructura de datos básica para el ejemplo
@dataclass
class SensorReading:
    sensor_id: str
    value: float
#Este funciona para poder tener una simulacion de un sensor



# ==========================================
# I - Principio de Segregación de la Interfaz (ISP)
# ==========================================

# Lo que establece este principio es el mantener las interfaces separadas
# Para asi solo utilizar las funciones que necesita tu sensor en este caso
# Y no tener que tener partes de codigo que no usaremos

class Readable(Protocol): #Ejemplos de funciones que se podrian utilizar
    def read(self) -> float: ...


class Writable(Protocol):
    def write(self, value: float) -> str: ...


class Calibratable(Protocol):
    def calibrate(self) -> float: ...


class Resettable(Protocol):
    def reset(self) -> bool:...


# ==========================================
# D - Principio de Inversión de Dependencias (DIP)
# ==========================================

# Lo que indica este principio es que las clases deben depender de interfaces o clases
# Abstractas en lugar de clases y funciones concretas
# Asi facilitando el cambio de la fuente sin causar problemas en el codigo

class DataRepository(Protocol):
    def save(self, reading: SensorReading) -> None: ... #Esta funcion se encarga de guardar que se usa despues
    def get_latest(self, sensor_id: str) -> SensorReading | None: ...

class DataProcessor:
    """Depende de la abstraccion, no de una implementacion concreta."""
    
    def __init__(self, repository: DataRepository) -> None:
        self._repo = repository # inyeccion de dependencias

    def process_reading(self, sensor_id: str, value: float) -> None:
        # Lógica de negocio simulada
        reading = SensorReading(sensor_id=sensor_id, value=value)
        self._repo.save(reading) #Aqui se usa el DataRepository, si este llegara a cambiar este codigo no cambia

# --- Ejemplos de Implementaciones Concretas ---

class PostgreSQLRepository:
    def save(self, reading: SensorReading) -> None:
        print(f"Guardando {reading.value} del sensor {reading.sensor_id} en PostgreSQL...")

    def get_latest(self, sensor_id: str) -> SensorReading | None:
        return SensorReading(sensor_id, 25.0)

class InMemoryRepository:
    def __init__(self) -> None:
        self._db: dict[str, SensorReading] = {}

    def save(self, reading: SensorReading) -> None:
        self._db[reading.sensor_id] = reading
        print(f"Guardando {reading.value} en diccionario de memoria (Test)...")

    def get_latest(self, sensor_id: str) -> SensorReading | None:
        return self._db.get(sensor_id)

# En produccion: processor = DataProcessor(PostgreSQLRepository())
# En tests: processor = DataProcessor(InMemoryRepository()) <- sin base de datos