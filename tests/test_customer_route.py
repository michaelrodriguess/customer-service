from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from pytest import fixture

from main import app
from routes.customer_router import get_customer_service


@fixture(name="service")
def fixture_service():
    """
    The mock service simulates the behavior of the `CustomerService` class,
    enabling testing of FastAPI routes without relying on the actual service logic.
    """
    return MagicMock()


@fixture(name="client")
def fixture_client(service):
    """
    The test client overrides the `get_customer_service` dependency in the application
    with the mocked `service` fixture, allowing tests to simulate API interactions.
    """
    app.dependency_overrides[get_customer_service] = lambda: service
    client = TestClient(app)
    return client


@fixture(name="customer_json")
def fixture_customer_json():
    """
    This customer data represents a fictional customer and is used in tests
    to validate API responses and functionality.
    """
    return {
        "id": "01F8MECHZX3TBDSZ7XD96VR2H5",
        "name": "John Doe",
        "email": "johndoe@example.com",
        "active": True,
        "created_at": "2024-01-01T12:00:00",
        "updated_at": None,
    }


def test_router_get_all_customers(service, client, customer, customer_json):
    """
    This test verifies that the route returns the correct JSON response for all customers
    and ensures that the `get_all_customers` method of the mocked service is called once.
    """
    service.get_all_customers.return_value = [customer]
    response = client.get("/customers")

    assert response.status_code == 200
    assert response.json() == [customer_json]
    service.get_all_customers.assert_called_once()


def test_router_get_customer_by_id(service, client, customer, customer_json):
    """
    This test verifies that the route returns the correct JSON response for a customer
    and ensures that the `get_customer_by_id` method of the mocked service is called with the correct ID.
    """
    service.get_customer_by_id.return_value = customer
    response = client.get("/customers/01F8MECHZX3TBDSZ7XD96VR2H5")

    assert response.status_code == 200
    assert response.json() == customer_json
    service.get_customer_by_id.assert_called_once_with("01F8MECHZX3TBDSZ7XD96VR2H5")


def test_router_get_customer_by_id_value_error(service, client):
    """
    This test verifies that the route handles a `ValueError` raised by the mocked service
    and returns the appropriate status code.
    """
    service.get_customer_by_id.side_effect = ValueError()
    response = client.get("/customers/01F8MECHZX3TBDSZ7XD96VR2H5")

    assert response.status_code == 404
    service.get_customer_by_id.assert_called_once_with("01F8MECHZX3TBDSZ7XD96VR2H5")
