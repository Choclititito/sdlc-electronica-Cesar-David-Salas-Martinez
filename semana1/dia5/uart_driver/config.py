# config.py
#Importamos la librería dataclasses para crear una clase inmutable que represente la configuración del UART
from dataclasses import dataclass


@dataclass(frozen=True) # El frozen hace que la clase sea inmutable, y que sus atributos no se puedan modificar despues de creados
class UartConfig: #Aqui ponemos la configuracion que debe tener el uart para funcionar
    baudrate: int
    parity: str
    stop_bits: int
    timeout: float

    def __post_init__(self) -> None:
        # Responsabilidad Única: Solo valida la configuración al nacer
        if self.baudrate not in (9600, 19200, 38400, 115200):
            raise ValueError(f"Baudrate inválido: {self.baudrate}")
        if self.parity not in ('N', 'E', 'O'):
            raise ValueError(f"Paridad inválida: {self.parity}") #Manda los errores si la configuracion no es correcta