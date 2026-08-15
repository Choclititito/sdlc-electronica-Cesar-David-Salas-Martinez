"""test_api_integration.py
Dia 5
Codigo para definir las pruebas de integracion de la API
Se encarga de definir las pruebas de integracion para los endpoints de la API"""


# --- health ---
# Test para verificar que la API esta funcionando correctamente
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# --- sensores: creación ---
# Test para verificar que se puede crear un sensor correctamente
def test_create_sensor(client):
    response = client.post(
        "/sensors",
        json={
            "sensor_id": "TEMP-01",
            "sensor_type": "temperature",
            "unit": "C",
        },
    )
    assert response.status_code == 201
    assert response.json()["sensor_id"] == "TEMP-01"


# Test para verificar que no se puede crear un sensor con el mismo ID
def test_create_sensor_duplicate_returns_409(client):
    client.post(
        "/sensors",
        json={"sensor_id": "TEMP-01", "sensor_type": "temperature", "unit": "C"},
    )
    response = client.post(
        "/sensors",
        json={"sensor_id": "TEMP-01", "sensor_type": "temperature", "unit": "C"},
    )
    assert response.status_code == 409


# Test para verificar que no se puede crear un sensor con un tipo de unidad que no
# coincide con el tipo de sensor
def test_create_sensor_unit_type_mismatch_returns_422(client):
    response = client.post(
        "/sensors",
        json={"sensor_id": "TEMP-01", "sensor_type": "humidity", "unit": "C"},
    )
    assert response.status_code == 422


# Test para verificar que no se puede crear un sensor con un tipo de unidad desconocido
def test_create_sensor_unknown_unit_returns_422(client):
    response = client.post(
        "/sensors",
        json={"sensor_id": "TEMP-01", "sensor_type": "temperature", "unit": "psi"},
    )
    assert response.status_code == 422


# --- sensores: lectura y listado ---
# Test para verificar que se puede obtener un sensor correctamente
def test_get_sensor_not_found_returns_404(client):
    response = client.get("/sensors/DOES-NOT-EXIST")
    assert response.status_code == 404


# Test para verificar que se puede obtener un sensor correctamente
def test_get_sensor_happy_path(client):
    client.post(
        "/sensors",
        json={"sensor_id": "TEMP-01", "sensor_type": "temperature", "unit": "C"},
    )
    response = client.get("/sensors/TEMP-01")
    assert response.status_code == 200
    assert response.json()["unit"] == "C"


# Test para verificar que se puede listar los sensores correctamente
def test_list_sensors(client):
    client.post(
        "/sensors",
        json={"sensor_id": "TEMP-01", "sensor_type": "temperature", "unit": "C"},
    )
    client.post(
        "/sensors", json={"sensor_id": "HUM-01", "sensor_type": "humidity", "unit": "%"}
    )
    response = client.get("/sensors")
    assert response.status_code == 200
    ids = {s["sensor_id"] for s in response.json()}
    assert ids == {"TEMP-01", "HUM-01"}


# Test para verificar que se puede listar los sensores correctamente con paginacion
def test_list_sensors_pagination(client):
    for i in range(3):
        client.post(
            "/sensors",
            json={"sensor_id": f"TEMP-0{i}", "sensor_type": "temperature", "unit": "C"},
        )
    response = client.get("/sensors?limit=2&offset=1")
    assert response.status_code == 200
    assert len(response.json()) == 2


# --- sensores: actualización parcial ---
# Test para verificar que se puede actualizar un sensor correctamente
def test_update_sensor(client):
    client.post(
        "/sensors",
        json={"sensor_id": "TEMP-01", "sensor_type": "temperature", "unit": "C"},
    )
    response = client.patch(
        "/sensors/TEMP-01", json={"unit": "F", "sensor_type": "temperature"}
    )
    assert response.status_code == 200
    assert response.json()["unit"] == "F"


# Test para verificar que no se puede actualizar un sensor que no existe
def test_update_sensor_not_found_returns_404(client):
    response = client.patch("/sensors/GHOST-01", json={"unit": "F"})
    assert response.status_code == 404


# --- sensores: borrado (desactivación) ---
# Test para verificar que se puede borrar un sensor correctamente
def test_delete_sensor(client):
    client.post(
        "/sensors",
        json={"sensor_id": "TEMP-01", "sensor_type": "temperature", "unit": "C"},
    )
    response = client.delete("/sensors/TEMP-01")
    assert response.status_code == 204


# Test para verificar que no se puede borrar un sensor que no existe
def test_delete_sensor_not_found_returns_404(client):
    response = client.delete("/sensors/GHOST-01")
    assert response.status_code == 404


# Test para verificar que un sensor desactivado no aparece en el listado de sensores
def test_deactivated_sensor_disappears_from_list(client):
    client.post(
        "/sensors",
        json={"sensor_id": "TEMP-01", "sensor_type": "temperature", "unit": "C"},
    )
    client.delete("/sensors/TEMP-01")
    response = client.get("/sensors")
    assert response.json() == []


# --- lecturas: creación ---
# Test para verificar que no se puede crear una lectura para un sensor que no existe
def test_create_reading_for_unknown_sensor_returns_404(client):
    response = client.post(
        "/sensors/GHOST-01/readings",
        json={
            "sensor_id": "GHOST-01",
            "value": 20.0,
            "unit": "C",
        },
    )
    assert response.status_code == 404


# Test para verificar que se puede crear una lectura correctamente
def test_create_reading_happy_path(client):
    client.post(
        "/sensors",
        json={"sensor_id": "TEMP-01", "sensor_type": "temperature", "unit": "C"},
    )
    response = client.post(
        "/sensors/TEMP-01/readings",
        json={
            "sensor_id": "TEMP-01",
            "value": 22.5,
            "unit": "C",
        },
    )
    assert response.status_code == 201
    assert response.json()["value"] == 22.5


# Test para verificar que no se puede crear una lectura con una unidad que no coincide
# con la del sensor
def test_create_reading_unknown_unit_returns_422(client):
    client.post(
        "/sensors",
        json={"sensor_id": "TEMP-01", "sensor_type": "temperature", "unit": "C"},
    )
    response = client.post(
        "/sensors/TEMP-01/readings",
        json={
            "sensor_id": "TEMP-01",
            "value": 20.0,
            "unit": "psi",
        },
    )
    assert response.status_code == 422


# Test para verificar que no se puede crear una lectura con un valor fuera del rango
# físico del sensor
def test_create_reading_out_of_physical_range_returns_422(client):
    client.post(
        "/sensors",
        json={"sensor_id": "TEMP-01", "sensor_type": "temperature", "unit": "C"},
    )
    response = client.post(
        "/sensors/TEMP-01/readings",
        json={
            "sensor_id": "TEMP-01",
            "value": -300.0,
            "unit": "C",
        },
    )
    assert response.status_code == 422


# --- lecturas: listado con filtros de fecha ---
# Test para verificar que se puede listar las lecturas de un sensor correctamente
def test_list_readings_for_sensor(client):
    client.post(
        "/sensors",
        json={"sensor_id": "TEMP-01", "sensor_type": "temperature", "unit": "C"},
    )
    client.post(
        "/sensors/TEMP-01/readings",
        json={"sensor_id": "TEMP-01", "value": 20.0, "unit": "C"},
    )
    client.post(
        "/sensors/TEMP-01/readings",
        json={"sensor_id": "TEMP-01", "value": 21.0, "unit": "C"},
    )
    response = client.get("/sensors/TEMP-01/readings")
    assert response.status_code == 200
    assert len(response.json()) == 2


# Test para verificar que se obtiene un 404 al listar lecturas de un sensor que
# no existe
def test_list_readings_unknown_sensor_returns_404(client):
    response = client.get("/sensors/GHOST-01/readings")
    assert response.status_code == 404


# Test para verificar que se obtiene un 400 al listar lecturas con un rango de fechas
# inválido
def test_list_readings_invalid_date_range_returns_400(client):
    client.post(
        "/sensors",
        json={"sensor_id": "TEMP-01", "sensor_type": "temperature", "unit": "C"},
    )
    response = client.get(
        "/sensors/TEMP-01/readings?from=2026-12-31T00:00:00&to=2026-01-01T00:00:00"
    )
    assert response.status_code == 400


# Test para verificar que se puede listar las lecturas de un sensor correctamente con un
#  rango de fechas válido
def test_list_readings_with_valid_date_range(client):
    client.post(
        "/sensors",
        json={"sensor_id": "TEMP-01", "sensor_type": "temperature", "unit": "C"},
    )
    client.post(
        "/sensors/TEMP-01/readings",
        json={"sensor_id": "TEMP-01", "value": 20.0, "unit": "C"},
    )
    response = client.get(
        "/sensors/TEMP-01/readings?from=2020-01-01T00:00:00&to=2030-01-01T00:00:00"
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


# Test para verificar que se puede listar las lecturas de un sensor correctamente con
# paginacion
def test_list_readings_pagination(client):
    client.post(
        "/sensors",
        json={"sensor_id": "TEMP-01", "sensor_type": "temperature", "unit": "C"},
    )
    for v in (10.0, 11.0, 12.0):
        client.post(
            "/sensors/TEMP-01/readings",
            json={"sensor_id": "TEMP-01", "value": v, "unit": "C"},
        )
    response = client.get("/sensors/TEMP-01/readings?limit=1&offset=1")
    assert response.status_code == 200
    assert len(response.json()) == 1


# --- lecturas: obtención individual ---
# Test para verificar que se obtiene un 404 al obtener una lectura que no existe
def test_get_reading_not_found_returns_404(client):
    response = client.get("/readings/999")
    assert response.status_code == 404


# --- lecturas: ciclo completo (GET, PATCH, DELETE) ---
# Test para verificar que se puede realizar un ciclo completo de operaciones sobre una
# lectura
def test_full_reading_lifecycle(client):
    client.post(
        "/sensors",
        json={"sensor_id": "TEMP-01", "sensor_type": "temperature", "unit": "C"},
    )
    created = client.post(
        "/sensors/TEMP-01/readings",
        json={
            "sensor_id": "TEMP-01",
            "value": 20.0,
            "unit": "C",
        },
    ).json()
    reading_id = created["id"]

    get_resp = client.get(f"/readings/{reading_id}")
    assert get_resp.status_code == 200

    patch_resp = client.patch(f"/readings/{reading_id}", json={"value": 21.0})
    assert patch_resp.status_code == 200
    assert patch_resp.json()["value"] == 21.0

    delete_resp = client.delete(f"/readings/{reading_id}")
    assert delete_resp.status_code == 204


# Test para verificar que se obtiene un 404 al intentar obtener una lectura que ha sido
# borrada
def test_update_reading_not_found_returns_404(client):
    response = client.patch("/readings/999", json={"value": 20.0})
    assert response.status_code == 404


# Test para verificar que se obtiene un 400 al intentar actualizar una lectura con un
# valor fuera del rango físico del sensor
def test_update_reading_below_absolute_zero_returns_400(client):
    client.post(
        "/sensors",
        json={"sensor_id": "TEMP-01", "sensor_type": "temperature", "unit": "C"},
    )
    created = client.post(
        "/sensors/TEMP-01/readings",
        json={
            "sensor_id": "TEMP-01",
            "value": 20.0,
            "unit": "C",
        },
    ).json()
    response = client.patch(f"/readings/{created['id']}", json={"value": -300.0})
    assert response.status_code == 400


# Test para verificar que se obtiene un 404 al intentar borrar una lectura que no existe
def test_delete_reading_not_found_returns_404(client):
    response = client.delete("/readings/999")
    assert response.status_code == 404
