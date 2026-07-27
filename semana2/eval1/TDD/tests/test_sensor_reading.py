import unittest
from datetime import datetime

from sensor_reading import SensorReading, InvalidReadingError


class TestSensorReading(unittest.TestCase):

    def test_crea_lectura_valida(self):
        ts = datetime(2026, 7, 26, 10, 0, 0)
        r = SensorReading(sensor_id="S01", temperature=28.5, humidity=55.0, timestamp=ts)
        self.assertEqual(r.sensor_id, "S01")
        self.assertEqual(r.temperature, 28.5)
        self.assertEqual(r.humidity, 55.0)
        self.assertEqual(r.timestamp, ts)
        self.assertTrue(r.is_valid())

    def test_lectura_en_limites_validos_es_valida(self):
        r = SensorReading(sensor_id="S02", temperature=-40.0, humidity=0.0, timestamp=datetime.now())
        self.assertTrue(r.is_valid())
        r2 = SensorReading(sensor_id="S02", temperature=80.0, humidity=100.0, timestamp=datetime.now())
        self.assertTrue(r2.is_valid())

    def test_temperatura_fuera_de_rango_fisico_no_es_valida(self):
        r = SensorReading(sensor_id="S03", temperature=-50.0, humidity=40.0, timestamp=datetime.now())
        self.assertFalse(r.is_valid())

    def test_humedad_fuera_de_rango_fisico_no_es_valida(self):
        r = SensorReading(sensor_id="S03", temperature=25.0, humidity=150.0, timestamp=datetime.now())
        self.assertFalse(r.is_valid())

    def test_sensor_id_vacio_lanza_error(self):
        with self.assertRaises(InvalidReadingError):
            SensorReading(sensor_id="", temperature=25.0, humidity=40.0, timestamp=datetime.now())

    def test_temperatura_no_numerica_lanza_error(self):
        with self.assertRaises(InvalidReadingError):
            SensorReading(sensor_id="S01", temperature="caliente", humidity=40.0, timestamp=datetime.now())

    def test_to_dict_serializa_correctamente(self):
        ts = datetime(2026, 7, 26, 10, 0, 0)
        r = SensorReading(sensor_id="S01", temperature=28.5, humidity=55.0, timestamp=ts)
        d = r.to_dict()
        self.assertEqual(d["sensor_id"], "S01")
        self.assertEqual(d["temperature"], 28.5)
        self.assertEqual(d["humidity"], 55.0)
        self.assertEqual(d["timestamp"], ts.isoformat())


if __name__ == "__main__":
    unittest.main()
