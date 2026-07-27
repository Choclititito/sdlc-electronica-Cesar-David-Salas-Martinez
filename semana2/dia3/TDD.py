# 2) GREEN - el codigo minimo que lo hace pasar

import pytest

class SensorNotFoundError(Exception):
    pass

class SensorRegistry:
    def get(self, sensor_id: str):
        raise SensorNotFoundError(f"Sensor {sensor_id} not found")

def test_get_unknown_sensor_raises():
    registry = SensorRegistry()
    with pytest.raises(SensorNotFoundError):
        registry.get("GHOST-99")
 
 

# git commit -am "feat: implementar SensorRegistry (GREEN) - us-01"
 
