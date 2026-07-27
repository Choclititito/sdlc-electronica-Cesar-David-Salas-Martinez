"""Testeos de los ejemplos correctos"""


from solid_srp_ocp_lsp import (
    AlertStrategy,
    ConsoleAlert,
    EmailAlert,
    EmailAlerter,
    HumiditySensor,
    SensorReader,
    TemperatureSensor,
)

"""Primer principio S - Principio de Responsabilidad Unica"""


def test_sensor_reader_retorna_valor_esperado():
    # 1. Preparación y Aislamiento
    lector = SensorReader()
    
    # 2. Aserción: Verificamos el valor exacto de la simulación
    assert lector.read_data() == 25.5

def test_email_alert():
    emailalert = EmailAlerter()

    assert emailalert.send_alert() == "Enviando correo de alerta..."

"""Segundo principio O - Principio Abierto/Cerrado"""
def test_console_alert_cumple_contrato_estrategia():
    # 1. Preparación
    alerta_consola = ConsoleAlert()
    
    # 2. Aserción: Confirmamos que la clase hija es oficialmente reconocida 
    # como una AlertStrategy (cumple el contrato)
    assert isinstance(alerta_consola, AlertStrategy)

def test_email_alert_cumple_contrato_estrategia():
    # 1. Preparación
    alerta_email = EmailAlert()
    
    # 2. Aserción: Confirmamos que esta nueva extensión también 
    # es reconocida como una estrategia válida
    assert isinstance(alerta_email, AlertStrategy)


"""Tercer principio L - Principio de Sustitucion de Liskov"""
def test_temperature_sensor_respeta_firma_liskov():
    # 1. Preparación
    sensor_temp = TemperatureSensor()
    
    # 2. Aserción: Verificamos que la clase hija devuelva exactamente 
    # el tipo de dato (float) que promete la clase base BaseSensor
    assert type(sensor_temp.get_reading()) is float
    assert sensor_temp.get_reading() == 25.5

def test_humidity_sensor_respeta_firma_liskov():
    # 1. Preparación
    sensor_humedad = HumiditySensor()
    
    # 2. Aserción: Verificamos que esta otra clase hija también sea intercambiable
    # y no rompa el contrato matemático devolviendo otro tipo de dato
    assert type(sensor_humedad.get_reading()) is float
    assert sensor_humedad.get_reading() == 60.2