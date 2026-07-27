# 3) REFACTOR - mejorar con los tests en verde

import pytest #Importamos la libreria para poder hacer las pruebas

class SensorNotFoundError(Exception): #Definimos una clase para el mensaje de error
    """Excepción lanzada cuando se busca un sensor que no está registrado."""
    pass
class SensorRegistry:
    """Registro de sensores optimizado y refactorizado."""
    
    def _validate_sensor(self, sensor_id: str) -> None:
        # Extraemos la lógica de validación para cumplir con SRP (Responsabilidad Única)
        raise SensorNotFoundError(f"Sensor {sensor_id} not found")

    def get(self, sensor_id: str):
        # El método principal ahora delega la validación
        self._validate_sensor(sensor_id)

def test_get_unknown_sensor_raises():
    registry = SensorRegistry()
    with pytest.raises(SensorNotFoundError):
        registry.get("GHOST-99")
 


# git commit -am "refactor: extraer validacion en SensorRegistry"