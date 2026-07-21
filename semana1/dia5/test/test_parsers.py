#test_parsers.py
#Importamos los modulos desde la carpeta uart_driver

from uart_driver.parsers import ModbusParser, NMEAParser #Importamos los parsers que vamos a testear

# --- Tests para ModbusParser ---
def test_modbus_frame_valido(): #Checamos que el parser reconoce correctamente una trama Modbus valida
    parser = ModbusParser()
    assert parser.can_parse(b'\x01\x03\x00\x00') is True

def test_modbus_frame_invalido(): #Vemos que pasa cuando le pasamos una trama que no es Modbus
    parser = ModbusParser()
    # Falla por ser muy corto y no empezar con \x01
    assert parser.can_parse(b'\x02\x03') is False

def test_modbus_parse_payload(): #Probamos que el parser puede parsear correctamente una trama Modbus y extraer el payload
    parser = ModbusParser()
    resultado = parser.parse(b'\x01\x03\x00\x00')
    assert resultado["protocol"] == "Modbus RTU"
    assert resultado["payload"] == "01030000"

# --- Tests para NMEAParser ---
def test_nmea_frame_valido(): #Checamos que el parser reconoce correctamente una trama NMEA valida
    parser = NMEAParser()
    assert parser.can_parse(b'$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M*47') is True

def test_nmea_frame_invalido(): #Vemos que pasa cuando le pasamos una trama que no es NMEA
    parser = NMEAParser()
    # Falla porque la sentencia GPS no es GPGGA
    assert parser.can_parse(b'$GPGSV,3,1,11,03,03,111*74') is False

def test_nmea_parse_payload(): #Probamos que el parser puede parsear correctamente una trama NMEA y extraer el payload
    parser = NMEAParser()
    resultado = parser.parse(b'$GPGGA,123456\r\n')
    assert resultado["protocol"] == "NMEA GPS"
    assert resultado["payload"] == "$GPGGA,123456"