# parsers.py

#Importamos librerias que usaremos
from abc import ABC, abstractmethod
from typing import Any


class MessageParser(ABC): # Clase abstracta para los analizadores de mensaje
    @abstractmethod
    def can_parse(self, raw_data: bytes) -> bool:
        ...
        
    @abstractmethod
    def parse(self, raw_data: bytes) -> dict[str, Any]:
        ...

class ModbusParser(MessageParser): #clase que implementa el analizador de mensajes Modbus RTU
    def can_parse(self, raw_data: bytes) -> bool:
        # Detectamos de manera simple el inicio de trama Modbus RTU
        return len(raw_data) >= 4 and raw_data.startswith(b'\x01') 
        
    def parse(self, raw_data: bytes) -> dict[str, Any]:
        return {"protocol": "Modbus RTU", "payload": raw_data.hex()}

class NMEAParser(MessageParser): #clase que implementa el analizador de mensajes NMEA GPS
    def can_parse(self, raw_data: bytes) -> bool:
        # Detectamos la sentencia de GPS NMEA
        return raw_data.startswith(b'$GPGGA')
        
    def parse(self, raw_data: bytes) -> dict[str, Any]:
        return {"protocol": "NMEA GPS", "payload": raw_data.decode('ascii', errors='ignore').strip()}