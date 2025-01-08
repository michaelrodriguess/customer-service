from unittest.mock import MagicMock

import pytest
from psycopg2 import DatabaseError
from pytest import fixture

from services.customer_service import CustomerService


@fixture(name="mock_storage")
def fixture_mock_storage():
    """
    Fixture that provides a mocked storage object.
    """
    return MagicMock()


@fixture(name="service")
def fixture_service(mock_storage):
    """
    Fixture that provides an instance of `CustomerService` using a mocked storage.
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
