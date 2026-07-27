#test_recorder.py
#Importamos los modulos desde la carpeta uart_driver y otro paquete necesario para las pruebas

import json

from uart_driver.recorder import (
    DataRecorder,  #Importamos la clase DataRecorder que se encarga de guardar los datos en un archivo JSON-Lines
)


def test_recorder_creacion(tmp_path): #Verificamos que el DataRecorder se crea correctamente con la ruta de archivo proporcionada
    # tmp_path proporciona una ruta temporal segura
    archivo = tmp_path / "datos.jsonl"
    recorder = DataRecorder(str(archivo))
    assert recorder._filepath == str(archivo)

def test_recorder_escritura_json_valida(tmp_path): #Probamos que el DataRecorder guarda correctamente un diccionario como JSON en el archivo
    archivo = tmp_path / "datos.jsonl"
    recorder = DataRecorder(str(archivo))
    
    # Guardamos un diccionario (simulando el resultado de un parser)
    datos = {"protocol": "Modbus RTU", "payload": "1234"}
    recorder.save(datos)
    
    # Leemos el archivo físico para comprobar que el JSON se escribió
    with open(archivo, encoding='utf-8') as f:
        lineas = f.readlines()
        assert len(lineas) == 1
        # Convertimos el texto JSON de vuelta a diccionario para afirmarlo
        dato_guardado = json.loads(lineas[0])
        assert dato_guardado["protocol"] == "Modbus RTU"

def test_recorder_escritura_multiple_append(tmp_path): #Verificamos que el DataRecorder puede guardar múltiples diccionarios en el mismo archivo sin sobrescribir los anteriores
    archivo = tmp_path / "datos.jsonl"
    recorder = DataRecorder(str(archivo))
    
    recorder.save({"id": 1, "tipo": "A"})
    recorder.save({"id": 2, "tipo": "B"})
    
    # Verificamos que se guarden ambas líneas (JSON-Lines) sin sobrescribirse
    with open(archivo, encoding='utf-8') as f:
        lineas = f.readlines()
        assert len(lineas) == 2
        assert json.loads(lineas[0])["id"] == 1
        assert json.loads(lineas[1])["id"] == 2