# recorder.py
#Importaciones que usaremos
import json
from typing import Any

class DataRecorder: #Clase para guardar los datos en un archivo
    def __init__(self, filepath: str) -> None:
        self._filepath = filepath
        
    def save(self, data: dict[str, Any]) -> None:
        # Persiste las lecturas validas en formato JSON-Lines
        with open(self._filepath, 'a', encoding='utf-8') as f:
            f.write(json.dumps(data) + '\n') #Aqui mandamos a guardar los datos en el archivo en formato JSON-Lines