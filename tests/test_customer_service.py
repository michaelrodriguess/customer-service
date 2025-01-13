"""
This module contains tests for the CustomerService class.
"""
from unittest.mock import MagicMock
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


def test_get_customer_by_email(service, customer):
    """
    Test if the email given is the same as customer, and calls storage.
    """
    customer_email = "johndoe@example.com"

    service.storage.get_customer_by_email.return_value = customer

    result = service.storage.get_customer_by_email(customer_email)
    assert result == customer
    service.storage.get_customer_by_email.assert_called_once_with(customer_email)
