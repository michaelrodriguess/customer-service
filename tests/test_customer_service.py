"""
This module contains tests for the CustomerService class.
"""
from unittest.mock import MagicMock
import pytest
from pytest import fixture, raises
from psycopg2 import DatabaseError

from services.customer_service import CustomerService


@fixture(name="mock_storage")
def fixture_mock_storage():
    """
        Provides a mocked CustomerStorage instance.
    """
    return MagicMock()


@fixture(name="service")
def fixture_service(mock_storage):
    """
    Provides a CustomerService instance with mocked storage.
    """
    return CustomerService(mock_storage)


def test_get_customer_by_id_successfully(customer, mock_storage, service):
    """
    Tests that the `get_customer_by_id` method retrieves the correct customer
    when a valid customer ID is provided.
    """
    mock_storage.get_customer_by_id.return_value = customer

    result = service.get_customer_by_id("01F8MECHZX3TBDSZ7XD96VR2H5")
    assert result == customer
    mock_storage.get_customer_by_id.assert_called_once_with("01F8MECHZX3TBDSZ7XD96VR2H5")

def test_get_customer_by_id_handles_value_error(mock_storage, service):
    """
    Tests that the `get_customer_by_id` method raises a `ValueError`
    when provided with an invalid customer ID.
    """
    mock_storage.get_customer_by_id.side_effect = ValueError()

    with pytest.raises(ValueError):
        service.get_customer_by_id("01F8MECHZX3TBDSZ7XD96VR2H0")

    mock_storage.get_customer_by_id.assert_called_once_with("01F8MECHZX3TBDSZ7XD96VR2H0")


def test_get_all_customers_successfully(customer, mock_storage, service):
    """
    Tests that the `get_all_customers` method correctly retrieves a list of customers
    from the underlying storage service.
    """
    mock_storage.get_all_customers.return_value = [customer]

    result = service.get_all_customers()
    assert result == [customer]
    mock_storage.get_all_customers.assert_called_once()


def test_get_all_customers_handles_database_error(mock_storage, service):
    """
    Tests that the `get_all_customers` method raises a `DatabaseError`
    when the underlying storage encounters a database issue.
    """
    mock_storage.get_all_customers.side_effect = DatabaseError()

    with pytest.raises(DatabaseError):
        service.get_all_customers()

    mock_storage.get_all_customers.assert_called_once()

def test_create_customer_success(customer, mock_storage, service):
    """
    Test the successful creation of a customer in the service layer.
    """
    mock_storage.create_customer.return_value = customer

    result = service.create_customer(customer)
    assert result == customer
    mock_storage.create_customer.assert_called_once_with(customer)


def test_create_customer_database_error(customer, mock_storage, service):
    """
    Test the DatabaseError when creating a customer in the service layer.
    """
    mock_storage.create_customer.side_effect = DatabaseError()

    with raises(DatabaseError):
        service.create_customer(customer)

    mock_storage.create_customer.assert_called_once_with(customer)


def test_delete_customer_calls_storage(service):
    """
    Tests if the service calls the storage method to delete a customer.
    """
    customer_id = "01JGQ1XA2VW0K0WMTTJRXT5SXK"

    service.storage.delete_customer(customer_id)
    service.storage.delete_customer.assert_called_once_with(customer_id)


def test_delete_customer_key_error(service):
    """
    Tests if the service handles KeyError when deleting a customer.
    """
    customer_id = "01JGQ1XA2VW0K0WMTTJRXT5SXK"

    service.storage.delete_customer.side_effect = KeyError(
        "Simulating the KeyError")

    with raises(KeyError):
        service.delete_customer(customer_id)

    service.storage.delete_customer.assert_called_once()
