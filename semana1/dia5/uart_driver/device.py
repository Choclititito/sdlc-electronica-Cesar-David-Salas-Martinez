# device.py
from typing import Any

from uart_driver.config import (
    UartConfig,  #Importamos los datos de configuracion del uart
)
from uart_driver.parsers import (
    MessageParser,  #Importamos la clase abstracta de los analizadores de mensajes
)


class UartDevice:
    def __init__(self, config: UartConfig, parser: MessageParser) -> None:
        self._config = config #Uso de las importaciones
        self._parser = parser
        self._is_connected = False #Conexion inicial del dispositivo en falso
        
    def connect(self) -> None:
        # Lógica de conexión física (simulada aquí)
        print(f"Dispositivo conectado a {self._config.baudrate} baudios")
        self._is_connected = True
        
    def disconnect(self) -> None: #Simulacion de desconexion del dispositivo
        self._is_connected = False
        
    def read_and_parse(self, raw_data: bytes) -> dict[str, Any] | None:
        if not self._is_connected:
            raise ConnectionError("No se puede leer: UART desconectado.") #Caso de error
            
        if self._parser.can_parse(raw_data):
            return self._parser.parse(raw_data) #Si el analizador puede analizar los datos, se devuelve el resultado del análisis
        return None