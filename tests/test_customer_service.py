import pytest
from unittest.mock import MagicMock
from psycopg2 import DatabaseError, IntegrityError
from services.customer_service import CustomerService


@pytest.fixture(name="mock_storage")
def fixture_mock_storage():
    """
    Fixture that provides a mocked storage object.
    """
    return MagicMock()


@pytest.fixture(name="service")
def fixture_service(mock_storage):
    """
    Fixture that provides an instance of `CustomerService` using a mocked storage.
    """
    return CustomerService(mock_storage)


def test_create_customer_success(customer_create_row, mock_storage, service):
    mock_storage.create_customer.return_value = customer_create_row

    result = service.create_customer(customer_create_row)
    assert result == customer_create_row
    mock_storage.create_customer.assert_called_once_with(customer_create_row)


def test_create_customer_integrity_error(customer_create_row, mock_storage, service):
    mock_storage.create_customer.side_effect = IntegrityError()

    with pytest.raises(IntegrityError):
        service.create_customer(customer_create_row)

    mock_storage.create_customer.assert_called_once_with(customer_create_row)


def test_create_customer_database_error(customer_create_row, mock_storage, service):
    mock_storage.create_customer.side_effect = DatabaseError()

    with pytest.raises(DatabaseError):
        service.create_customer(customer_create_row)

    mock_storage.create_customer.assert_called_once_with(customer_create_row)