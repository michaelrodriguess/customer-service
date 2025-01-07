from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from pytest import fixture

from main import app
from routes.customer_router import get_customer_service


@fixture
def service():
    return MagicMock()


@fixture
def client(service):
    app.dependency_overrides[get_customer_service] = lambda: service
    client = TestClient(app)
    return client


@fixture
def customer_json():
    return {
        "id": "01F8MECHZX3TBDSZ7XD96VR2H5",
        "name": "John Doe",
        "email": "johndoe@example.com",
        "active": True,
        "created_at": "2024-01-01T12:00:00",
        "updated_at": None,
    }


def test_router_get_all_customers(service, client, customer, customer_json):
    service.get_all_customers.return_value = [customer]
    response = client.get("/customers")

    assert response.status_code == 200
    assert response.json() == [customer_json]
    service.get_all_customers.assert_called_once()


def test_router_get_customer_by_id(service, client, customer, customer_json):
    service.get_customer_by_id.return_value = customer
    response = client.get("/customers/01F8MECHZX3TBDSZ7XD96VR2H5")

    assert response.status_code == 200
    assert response.json() == customer_json
    service.get_customer_by_id.assert_called_once_with("01F8MECHZX3TBDSZ7XD96VR2H5")


def test_router_get_customer_by_id_value_error(service, client):
    service.get_customer_by_id.side_effect = ValueError()
    response = client.get("/customers/01F8MECHZX3TBDSZ7XD96VR2H5")

    assert response.status_code == 404
    service.get_customer_by_id.assert_called_once_with("01F8MECHZX3TBDSZ7XD96VR2H5")