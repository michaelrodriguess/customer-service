"""
This module contains tests for the customer-related routes in the FastAPI application.
"""

from unittest.mock import MagicMock
from pytest import fixture
from fastapi.testclient import TestClient
from main import app
from routes.customer_router import get_customer_service


@fixture(name="service")
def fixture_service():
    """
    The mock service simulates the behavior of the `CustomerService` class,
    enabling testing of FastAPI routes without relying on the actual service logic.
    Returns:
        MagicMock: A mocked instance of the CustomerService.
    """
    return MagicMock()


@fixture(name="client")
def fixture_client(service):
    """
    The test client overrides the `get_customer_service` dependency in the application
    with the mocked `service` fixture, allowing tests to simulate API interactions.
    Args:
        service (MagicMock): A mocked instance of the CustomerService.
    Returns:
        TestClient: A TestClient instance for simulating requests.
    """
    app.dependency_overrides[get_customer_service] = lambda: service
    client = TestClient(app)
    return client


@fixture(name="customer_json")
def fixture_customer_json():
    """
    This fixture provides a sample customer JSON object used in tests.
    Returns:
        dict: A dictionary representing a fictional customer.
    """
    return {
        "id": "01JFTE35ZRRZWCSKK6TBB1DZCT",
        "name": "Joaozin",
        "email": "joao-da-660@gmail.com",
        "active": True,
        "created_at": "2024-12-23T15:57:25.496623",
        "updated_at": None,
    }


def test_router_create_customer(service, client, customer_create_row, customer_json):
    """
    Test the creation of a customer through the FastAPI route.
    Verifies that the route correctly interacts with the service layer
    and returns the expected response.
    """
    service.create_customer.return_value = customer_json
    response = client.post("/customers", json=customer_json)

    assert response.status_code == 201
    assert response.json() == customer_json
    service.create_customer.assert_called_once_with(customer_create_row)
