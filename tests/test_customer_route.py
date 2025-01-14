"""
Tests for customer-related routes in the FastAPI application.
"""
from unittest.mock import MagicMock
from pytest import fixture
from fastapi.testclient import TestClient
from main import app
from routes.customer_router import get_customer_service


@fixture(name="service")
def fixture_service():
    """
    Mocked CustomerService instance.
    """
    return MagicMock()


@fixture(name="client")
def fixture_client(service):
    """
    Test client with mocked service dependency.
    """
    app.dependency_overrides[get_customer_service] = lambda: service
    client = TestClient(app)
    return client


@fixture(name="customer_json")
def fixture_customer_json():
    """
    Sample customer data for tests.
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

def test_router_create_customer(service, client, customer, customer_json):
    """
    Test customer creation route.
    """
    service.create_customer.return_value = customer_json
    response = client.post("/customers", json=customer_json)

    assert response.status_code == 201
    assert response.json() == customer_json
    service.create_customer.assert_called_once_with(customer)


def test_router_delete_customer(client, service):
    """
    Tests the deleting a customer route.
    """
    customer_id = "01JGQ1XA2VW0K0WMTTJRXT5SXK"

    service.delete_customer.return_value = None
    response = client.delete(f"/customers/{customer_id}")

    assert response.status_code == 204
    service.delete_customer.assert_called_once_with(customer_id)


def test_router_get_customer_by_email(client, service, customer_json):
    """
    Tests getting a customer by email.
    """
    customer_email = "johndoe@example.com"

    service.get_customer_by_email.return_value = customer_json
    response = client.get(f"/customers/email/{customer_email}")

    assert response.status_code == 200
    assert response.json() == customer_json
    service.get_customer_by_email.assert_called_once_with(customer_email)
