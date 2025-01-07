from unittest.mock import MagicMock

import pytest
from psycopg2 import DatabaseError
from pytest import fixture

from services.customer_service import CustomerService


@fixture
def mock_storage():
    return MagicMock()


@fixture
def service(mock_storage):
    return CustomerService(mock_storage)


def test_get_customer_by_id_successfully(customer, mock_storage, service):
    mock_storage.get_customer_by_id.return_value = customer

    result = service.get_customer_by_id("01F8MECHZX3TBDSZ7XD96VR2H5")
    assert result == customer
    mock_storage.get_customer_by_id.assert_called_once_with("01F8MECHZX3TBDSZ7XD96VR2H5")

def test_get_customer_by_id_handles_value_error(mock_storage, service):
    mock_storage.get_customer_by_id.side_effect = ValueError()

    with pytest.raises(ValueError):
        service.get_customer_by_id("01F8MECHZX3TBDSZ7XD96VR2H0")

    mock_storage.get_customer_by_id.assert_called_once_with("01F8MECHZX3TBDSZ7XD96VR2H0")


def test_get_all_customers_successfully(customer, mock_storage, service):
    mock_storage.get_all_customers.return_value = [customer]

    result = service.get_all_customers()
    assert result == [customer]
    mock_storage.get_all_customers.assert_called_once()


def test_get_all_customers_handles_database_error(mock_storage, service):
    mock_storage.get_all_customers.side_effect = DatabaseError()

    with pytest.raises(DatabaseError):
        service.get_all_customers()

    mock_storage.get_all_customers.assert_called_once()
