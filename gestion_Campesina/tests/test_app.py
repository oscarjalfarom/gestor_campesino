# tests/test_app.py
import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_crear_asociacion(client):
    response = client.post('/asociaciones', json={
        "id_asociacion": 1,
        "nombre_asociacion": "Asociación de Agricultores",
        "siglas": "ADA",
        "fecha_constitucion": "2023-01-01",
        "objetivo": "Fomentar la agricultura sostenible",
        "direccion": "Calle Falsa 123",
        "representante_legal": "Juan Pérez",
        "celular": "1234567890",
        "email": "contacto@ada.org"
    })
    assert response.status_code == 201
    assert response.get_json() == {"mensaje": "Asociación creada exitosamente"}
