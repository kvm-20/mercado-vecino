from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)


def test_health_responde_ok():
    respuesta = cliente.get("/health")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"estado": "ok"}


def test_pedido_invalido_se_rechaza():
    # total negativo: la validación falla antes de tocar la base de datos
    respuesta = cliente.post("/pedidos", json={"tienda_id": 1, "cliente": "Ana", "total": -5})
    assert respuesta.status_code == 422
