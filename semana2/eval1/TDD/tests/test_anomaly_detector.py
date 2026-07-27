import unittest
from datetime import datetime, timedelta

from sensor_reading import SensorReading
from anomaly_detector import AnomalyDetector, AnomalyType


def reading(sensor_id="S01", temperature=25.0, humidity=50.0, ts=None):  
#Creamos una función para crear lecturas de sensores con valores por defecto
    return SensorReading(
        sensor_id=sensor_id,
        temperature=temperature,
        humidity=humidity,
        timestamp=ts or datetime(2026, 7, 26, 10, 0, 0),
    )


class TestAnomalyDetectorUmbralesInyectados(unittest.TestCase):

    def test_umbrales_son_inyectados_no_hardcodeados(self):
        # Dos instancias con distintos umbrales deben comportarse distinto
        detector_estricto = AnomalyDetector(temperature_threshold=20.0, humidity_threshold=50.0)
        detector_laxo = AnomalyDetector(temperature_threshold=35.0, humidity_threshold=80.0)

        r = reading(temperature=25.0, humidity=60.0)

        eventos_estricto = detector_estricto.evaluate(r)
        eventos_laxo = detector_laxo.evaluate(r)

        self.assertTrue(len(eventos_estricto) > 0)
        self.assertEqual(len(eventos_laxo), 0)

    def test_no_existen_valores_por_defecto_ocultos_que_ignoren_el_umbral_inyectado(self):
    #Verifica que no existan valores por defecto ocultos que ignoren el umbral inyectado
        detector = AnomalyDetector(temperature_threshold=10.0, humidity_threshold=10.0)
        self.assertEqual(detector.temperature_threshold, 10.0)
        self.assertEqual(detector.humidity_threshold, 10.0)


class TestDeteccionAnomaliaTemperatura(unittest.TestCase):

    def setUp(self):
    #Creamos un detector de anomalias con umbrales especificos para temperatura y humedad
        self.detector = AnomalyDetector(temperature_threshold=35.0, humidity_threshold=80.0)

    def test_temperatura_supera_umbral_genera_anomalia(self):
    #Verifica que si la temperatura supera el umbral genera una anomalia
        r = reading(sensor_id="S03", temperature=36.2, humidity=40.0)
        eventos = self.detector.evaluate(r)
        self.assertEqual(len(eventos), 1)
        self.assertEqual(eventos[0].anomaly_type, AnomalyType.HIGH_TEMPERATURE)
        self.assertEqual(eventos[0].sensor_id, "S03")

    def test_temperatura_en_el_limite_exacto_no_genera_anomalia(self):
    #Verifica que si la temperatura esta en el limite exacto no genera anomalia
        r = reading(sensor_id="S03", temperature=35.0, humidity=40.0)
        eventos = self.detector.evaluate(r)
        self.assertEqual(len(eventos), 0)

    def test_anomalia_se_cierra_cuando_temperatura_vuelve_a_la_normalidad(self):
    #Verifica que la anomalia se cierra cuando la temperatura vuelve a la normalidad
        r1 = reading(sensor_id="S03", temperature=36.0, humidity=40.0, ts=datetime(2026, 7, 26, 10, 0, 0))
        self.detector.evaluate(r1)
        self.assertTrue(self.detector.has_active_anomaly("S03", AnomalyType.HIGH_TEMPERATURE))

        r2 = reading(sensor_id="S03", temperature=33.0, humidity=40.0, ts=datetime(2026, 7, 26, 10, 0, 30))
        eventos = self.detector.evaluate(r2)
        self.assertFalse(self.detector.has_active_anomaly("S03", AnomalyType.HIGH_TEMPERATURE))
        self.assertEqual(len(eventos), 0)


class TestDeteccionAnomaliaHumedad(unittest.TestCase):

    def setUp(self):
    #Creamos un detector de anomalias con umbrales especificos para temperatura y humedad
        self.detector = AnomalyDetector(temperature_threshold=35.0, humidity_threshold=80.0)
   
    def test_humedad_supera_umbral_genera_anomalia(self):
    #Verifica que si la humedad supera el umbral genera una anomalia
        r = reading(sensor_id="S07", temperature=25.0, humidity=85.0)
        eventos = self.detector.evaluate(r)
        self.assertEqual(len(eventos), 1)
        self.assertEqual(eventos[0].anomaly_type, AnomalyType.HIGH_HUMIDITY)
    def test_humedad_justo_por_debajo_del_umbral_no_genera_anomalia(self):
    #Verifica que si la humedad esta justo por debajo del umbral no genera anomalia
        r = reading(sensor_id="S07", temperature=25.0, humidity=79.9)
        eventos = self.detector.evaluate(r)
        self.assertEqual(len(eventos), 0)

    def test_temperatura_y_humedad_altas_simultaneas_generan_dos_eventos(self):
    #Verifica que si la temperatura y humedad son altas simultaneas generan dos eventos
        r = reading(sensor_id="S02", temperature=40.0, humidity=90.0)
        eventos = self.detector.evaluate(r)
        tipos = {e.anomaly_type for e in eventos}
        self.assertEqual(len(eventos), 2)
        self.assertIn(AnomalyType.HIGH_TEMPERATURE, tipos)
        self.assertIn(AnomalyType.HIGH_HUMIDITY, tipos)


class TestAnomalyDetectorLecturaInvalida(unittest.TestCase):

    def test_lectura_fuera_de_rango_fisico_se_ignora(self):
    #Verifica que una lectura fuera de rango fisico se ignora y no genera eventos
        detector = AnomalyDetector(temperature_threshold=35.0, humidity_threshold=80.0)
        r = reading(sensor_id="S09", temperature=-999.0, humidity=40.0)
        eventos = detector.evaluate(r)
        self.assertEqual(eventos, [])


if __name__ == "__main__":
    unittest.main()
