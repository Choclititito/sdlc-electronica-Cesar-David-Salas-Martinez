# 1) RED - el test primero; pytest DEBE fallar (ImportError)
def test_get_unknown_sensor_raises():
    registry = SensorRegistry()
    with pytest.raises(SensorNotFoundError):
        registry.get("GHOST-99")
 
# git commit -am "test: especificar SensorRegistry (RED) - us-01"
 
