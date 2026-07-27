import io
import os
import unittest
from datetime import datetime
from unittest.mock import patch

from anomaly_detector import AnomalyEvent, AnomalyType
from alert_manager import (
    AlertManager,
    AlertStrategy,
    ConsoleAlertStrategy,
    FileAlertStrategy,
)


def make_event(sensor_id="S01", anomaly_type=AnomalyType.HIGH_TEMPERATURE, value=36.5, threshold=35.0):
    return AnomalyEvent(
        sensor_id=sensor_id,
        anomaly_type=anomaly_type,
        value=value,
        threshold=threshold,
        timestamp=datetime(2026, 7, 26, 10, 0, 0),
        #Creamos un evento de anomalia con valores por defecto, para poder usarlo en los tests
    )


class TestAlertStrategyEsAbstracta(unittest.TestCase): 

    def test_no_se_puede_instanciar_alert_strategy_directamente(self):
        with self.assertRaises(TypeError):
            AlertStrategy() #Test para verificar que no se puede instanciar directamente

    def test_una_subclase_incompleta_tampoco_es_instanciable(self):
        class EstrategiaIncompleta(AlertStrategy):
            pass 

        with self.assertRaises(TypeError):
            EstrategiaIncompleta()
        #Test para verificar que una subclase incompleta tampoco es instanciable

class TestConsoleAlertStrategy(unittest.TestCase):
        #Verifica que si mande los datos a la consola
    def test_envia_alerta_a_stdout(self):
        strategy = ConsoleAlertStrategy()
        evento = make_event()
        with patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            strategy.send(evento)
            salida = fake_out.getvalue()
        self.assertIn("S01", salida)
        self.assertIn("temperatura_alta", salida)
        self.assertIn("36.5", salida)


class TestFileAlertStrategy(unittest.TestCase):
        #Verifica que si mande los datos a un archivo
    def setUp(self):
        self.filepath = "/tmp/test_alerts_iot.log"
        if os.path.exists(self.filepath):
            os.remove(self.filepath)

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.remove(self.filepath)

    def test_escribe_alerta_en_archivo(self):
        strategy = FileAlertStrategy(filepath=self.filepath)
        evento = make_event(sensor_id="S05", anomaly_type=AnomalyType.HIGH_HUMIDITY, value=88.0, threshold=80.0)
        strategy.send(evento)

        with open(self.filepath, "r", encoding="utf-8") as f:
            contenido = f.read()

        self.assertIn("S05", contenido)
        self.assertIn("humedad_alta", contenido)
        self.assertIn("88.0", contenido)

    def test_multiples_alertas_se_agregan_sin_sobrescribir(self):
        strategy = FileAlertStrategy(filepath=self.filepath)
        strategy.send(make_event(sensor_id="S01"))
        strategy.send(make_event(sensor_id="S02"))

        with open(self.filepath, "r", encoding="utf-8") as f:
            lineas = f.readlines()

        self.assertEqual(len(lineas), 2)


class DummyStrategy(AlertStrategy):
    """Estrategia de prueba para verificar que AlertManager delega correctamente."""
    def __init__(self):
        self.sent_events = []

    def send(self, event):
        self.sent_events.append(event)


class TestAlertManager(unittest.TestCase):

    def test_notifica_a_todas_las_estrategias_registradas(self):
    #Verifica que notifica a todas las estrategias registradas
        estrategia_a = DummyStrategy()
        estrategia_b = DummyStrategy()
        manager = AlertManager(strategies=[estrategia_a, estrategia_b])

        evento = make_event()
        manager.notify(evento)

        self.assertEqual(estrategia_a.sent_events, [evento])
        self.assertEqual(estrategia_b.sent_events, [evento])

    def test_no_reenvia_alerta_duplicada_para_la_misma_anomalia_activa(self):
    #Verifica que no reenvia alerta duplicada para la misma anomalia activa
        estrategia = DummyStrategy()
        manager = AlertManager(strategies=[estrategia])

        evento = make_event(sensor_id="S03")
        manager.notify(evento)
        # Misma anomalía activa (mismo sensor_id + tipo) llega de nuevo
        evento_repetido = make_event(sensor_id="S03", value=37.0)
        manager.notify(evento_repetido)

        self.assertEqual(len(estrategia.sent_events), 1)

    def test_anomalia_distinta_si_se_notifica(self):
    #Verifica que si es una anomalia distinta si se notifica
        estrategia = DummyStrategy()
        manager = AlertManager(strategies=[estrategia])

        manager.notify(make_event(sensor_id="S03", anomaly_type=AnomalyType.HIGH_TEMPERATURE))
        manager.notify(make_event(sensor_id="S03", anomaly_type=AnomalyType.HIGH_HUMIDITY))

        self.assertEqual(len(estrategia.sent_events), 2)

    def test_alerta_se_puede_reenviar_tras_resolver_la_anomalia(self):
    #Verifica que la alerta se puede reenviar tras resolver la anomalia
        estrategia = DummyStrategy()
        manager = AlertManager(strategies=[estrategia])

        manager.notify(make_event(sensor_id="S04"))
        manager.resolve(sensor_id="S04", anomaly_type=AnomalyType.HIGH_TEMPERATURE)
        manager.notify(make_event(sensor_id="S04"))

        self.assertEqual(len(estrategia.sent_events), 2)

    def test_manager_sin_estrategias_no_falla(self):
    #Verifica que el manager sin estrategias no falla
        manager = AlertManager(strategies=[])
        manager.notify(make_event())  # no debe lanzar excepción


if __name__ == "__main__": 
    unittest.main()
