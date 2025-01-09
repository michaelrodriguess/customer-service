from main import app
from pytest import fixture
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
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
    return{
        "id": "01JFTE35ZRRZWCSKK6TBB1DZCT",
        "name": "Joaozin",
        "email": "joao-da-660@gmail.com",
        "active": True,
        "created_at": "2024-12-23T15:57:25.496623",
        "updated_at": None,
    }


def test_router_create_customer(service, client, customer_create_row, customer_json):
    service.create_customer.return_value = customer_json
    response = client.post("/customers", json=customer_json)

    assert response.status_code == 201
    assert response.json() == customer_json
    service.create_customer.assert_called_once_with(customer_create_row)