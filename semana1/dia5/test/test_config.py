#test_config.py
#Importamos los modulos desde la carpeta uart_driver y otras paquetes necesarios para las pruebas
import pytest
from dataclasses import FrozenInstanceError
from uart_driver.config import UartConfig #Importamos la configuracion


def test_config_creacion_valida(): #Aqui se prueba la creacion de un objeto UartConfig con valores validos
    config = UartConfig(baudrate=115200, parity='N', stop_bits=1, timeout=0.5)
    assert config.baudrate == 115200 
    assert config.timeout == 0.5

def test_config_baudrate_invalido(): #Comprobamos que se lanza un ValueError al pasar un baudrate no permitido
    with pytest.raises(ValueError, match="Baudrate inválido"):
        UartConfig(baudrate=9999, parity='N', stop_bits=1, timeout=1.0)

def test_config_paridad_invalida(): #Comprobamos que se lanza un ValueError al pasar una paridad no permitida
    with pytest.raises(ValueError, match="Paridad inválida"):
        UartConfig(baudrate=9600, parity='Z', stop_bits=1, timeout=1.0)

def test_config_inmutabilidad(): #Probamos que el Frozen=true funciona correctamente y que no se pueden modificar los atributos despues de la creacion del objeto
    config = UartConfig(baudrate=9600, parity='N', stop_bits=1, timeout=1.0)
    
    with pytest.raises(FrozenInstanceError):
        config.baudrate = 19200