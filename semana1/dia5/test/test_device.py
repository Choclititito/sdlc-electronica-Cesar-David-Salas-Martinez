#test_device.py
#Importamos los modulos desde la carpeta uart_driver y otras paquetes necesarios para las pruebas

import pytest
from uart_driver.config import UartConfig #Importamos la configuracion
from uart_driver.parsers import ModbusParser #Importamos el parser que vamos a usar para las pruebas
from uart_driver.device import UartDevice #Importamos la parte de device como la conexion



def test_device_flujo_conexion(): # Probamos el flujo de conexion y desconexion del dispositivo UART
    config = UartConfig(baudrate=9600, parity='N', stop_bits=1, timeout=1.0)
    parser = ModbusParser()
    device = UartDevice(config, parser)
    
    assert device._is_connected is False
    device.connect()
    assert device._is_connected is True
    device.disconnect()
    assert device._is_connected is False

def test_device_lectura_sin_conectar(): #Probamos que el dispositivo no puede leer datos si no esta conectado
    config = UartConfig(baudrate=9600, parity='N', stop_bits=1, timeout=1.0)
    device = UartDevice(config, ModbusParser())
    
    # Prueba: intentar leer antes de llamar a connect() levanta un error
    with pytest.raises(ConnectionError, match="UART desconectado"):
        device.read_and_parse(b'\x01\x03')

def test_device_lectura_y_parseo_exitoso(): #Probamos que el dispositivo puede leer y parsear correctamente una trama Modbus
    config = UartConfig(baudrate=9600, parity='N', stop_bits=1, timeout=1.0)
    device = UartDevice(config, ModbusParser())
    device.connect()
    
    # Si inyectamos Modbus, debe saber leer tramas Modbus
    resultado = device.read_and_parse(b'\x01\x03\x00\x00')
    assert resultado is not None
    assert resultado["protocol"] == "Modbus RTU"

def test_device_ignora_basura(): #Probamos que el dispositivo ignora correctamente datos que no pertenecen al protocolo esperado
    config = UartConfig(baudrate=9600, parity='N', stop_bits=1, timeout=1.0)
    device = UartDevice(config, ModbusParser())
    device.connect()
    
    # Si inyectamos Modbus, debe devolver None ante un string NMEA
    resultado = device.read_and_parse(b'$GPGGA,123')
    assert resultado is None