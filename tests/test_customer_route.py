"""
Tests for customer-related routes in the FastAPI application.
"""

from unittest.mock import MagicMock
from pytest import fixture
from fastapi.testclient import TestClient
from main import app
from routes.customer_router import get_customer_service
from exceptions.customer_exceptions import EntityNotFound


@fixture(name="service")
def fixture_service():
    """
    Creates a mock service to simulate the behavior of the `CustomerService` class.
    This allows testing FastAPI routes without relying on the actual service logic.

    Returns:
        MagicMock: A mocked instance of the `CustomerService`.
    """
    return MagicMock()


@fixture(name="client")
def fixture_client(service):
    """
    Creates a FastAPI test client and overrides the `get_customer_service` dependency
    with the mocked service fixture.

    Args:
        service (MagicMock): A mocked instance of the `CustomerService`.

    Returns:
        TestClient: A test client for simulating HTTP requests.
    """
    app.dependency_overrides[get_customer_service] = lambda: service
    client = TestClient(app)
    return client


@fixture(name="customer_json")
def fixture_customer_json():
    """
    Provides sample customer data for testing purposes.

    Returns:
        dict: A dictionary containing sample customer details.
    """
    return {
        "id": "01F8MECHZX3TBDSZ7XD96VR2H5",
        "name": "John Doe",
        "email": "johndoe@example.com",
        "active": True,
        "created_at": "2024-01-01T12:00:00",
        "updated_at": None,
    }


@fixture(name="customer_put_update_json")
def customer_put_json():
    """
    Provides sample data for testing PUT updates to a customer.

    Returns:
        dict: A dictionary containing updated customer details.
    """
    return {
        "id": "01F8MECHZX3TBDSZ7XD96VR2H5",
        "name": "John Doe",
        "email": "johndoe@example.com",
        "active": True,
        "updated_at": "2024-01-01T00:00:00",
    }


@fixture(name="customer_patch_update_json")
def customer_patch_json():
    """
    Provides sample data for testing PATCH updates to a customer.

    Returns:
        dict: A dictionary containing partially updated customer details.
    """
    return {
        "id": "01F8MECHZX3TBDSZ7XD96VR2H5",
        "name": "John Doe",
        "email": "johndoe@example.com",
        "active": False,
        "updated_at": "2024-01-01T00:00:00",
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


def test_put_customer_success(
    service, client, customer_put_update, customer_put_update_json
):
    """
    Tests a successful PUT operation for updating a customer.

    Args:
        service (MagicMock): The mocked service.
        client (TestClient): The test client.
        customer_put_update (dict): Mocked return data for the PUT update.
        customer_put_update_json (dict): Input data for the PUT update.

    Asserts:
        - The response status code is 200.
        - The response JSON matches the expected updated customer data.
    """
    service.update_customer.return_value = customer_put_update
    response = client.put("/customers/", json=customer_put_update_json)

    assert response.status_code == 200
    assert response.json() == customer_put_update_json


def test_patch_customer_success(
    service, client, customer_patch_update, customer_patch_update_json
):
    """
    Tests a successful PATCH operation for partially updating a customer.

    Args:
        service (MagicMock): The mocked service.
        client (TestClient): The test client.
        customer_patch_update (dict): Mocked return data for the PATCH update.
        customer_patch_update_json (dict): Input data for the PATCH update.

    Asserts:
        - The response status code is 200.
        - The response JSON matches the expected partially updated customer data.
    """
    service.patch_customer.return_value = customer_patch_update
    response = client.patch("/customers/", json=customer_patch_update_json)

    assert response.status_code == 200
    assert response.json() == customer_patch_update_json


def test_put_customer_entity_not_found(client, service, customer_put_update_json):
    """
    Tests the PUT operation when the customer is not found.

    Args:
        client (TestClient): The test client.
        service (MagicMock): The mocked service.
        customer_put_update_json (dict): Input data for the PUT update.

    Asserts:
        - The response status code is 404.
    """
    service.update_customer.side_effect = EntityNotFound("Customer not found")
    response = client.put("/customers/", json=customer_put_update_json)
    assert response.status_code == 404


def test_patch_customer_entity_not_found(client, service, customer_patch_update_json):
    """
    Tests the PATCH operation when the customer is not found.

    Args:
        client (TestClient): The test client.
        service (MagicMock): The mocked service.
        customer (dict): Mocked return data for the PATCH update.
        customer_patch_update_json (dict): Input data for the PATCH update.

    Asserts:
        - The response status code is 404.
    """
    service.patch_customer.side_effect = EntityNotFound("Customer not found")
    response = client.patch("/customers/", json=customer_patch_update_json)
    assert response.status_code == 404


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
