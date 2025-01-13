"""
This module contains tests for the CustomerService class.
"""

from unittest.mock import MagicMock
from pytest import fixture, raises
from psycopg2 import DatabaseError, IntegrityError
from services.customer_service import CustomerService
from storages.customer_storage import CustomerStorage, EntityNotFound
from models.customer_model import Customer, CustomerUpdate


@fixture(name="mock_storage")
def fixture_mock_storage():
    """
    Provides a mocked CustomerStorage instance for testing purposes.

    Returns:
        MagicMock: A mocked instance of CustomerStorage.
    """
    return MagicMock()


@fixture(name="service")
def fixture_service(mock_storage):
    """
    Provides a CustomerService instance with a mocked storage layer.

    Args:
        mock_storage (MagicMock): A mocked CustomerStorage instance.

    Returns:
        CustomerService: An instance of CustomerService using the mocked storage.
    """
    return CustomerService(mock_storage)


def test_create_customer_success(customer_create_row, mock_storage, service):
    """
    Test the successful creation of a customer in the service layer.

    Verifies that the service correctly interacts with the storage layer
    to create a customer and returns the expected result.

    Args:
        customer_create_row (dict): The input data for creating a customer.
        mock_storage (MagicMock): The mocked storage layer.
        service (CustomerService): The CustomerService instance.
    """
    mock_storage.create_customer.return_value = customer_create_row

    result = service.create_customer(customer_create_row)
    assert result == customer_create_row
    mock_storage.create_customer.assert_called_once_with(customer_create_row)


def test_create_customer_integrity_error(customer_create_row, mock_storage, service):
    """
    Test the handling of IntegrityError when creating a customer.

    Verifies that the service raises IntegrityError and interacts with
    the storage layer as expected.

    Args:
        customer_create_row (dict): The input data for creating a customer.
        mock_storage (MagicMock): The mocked storage layer.
        service (CustomerService): The CustomerService instance.
    """
    mock_storage.create_customer.side_effect = IntegrityError()

    with raises(IntegrityError):
        service.create_customer(customer_create_row)

    mock_storage.create_customer.assert_called_once_with(customer_create_row)


def test_create_customer_database_error(customer_create_row, mock_storage, service):
    """
    Test the handling of DatabaseError when creating a customer.

    Verifies that the service raises DatabaseError and interacts with
    the storage layer as expected.

    Args:
        customer_create_row (dict): The input data for creating a customer.
        mock_storage (MagicMock): The mocked storage layer.
        service (CustomerService): The CustomerService instance.
    """
    mock_storage.create_customer.side_effect = DatabaseError()

    with raises(DatabaseError):
        service.create_customer(customer_create_row)

    mock_storage.create_customer.assert_called_once_with(customer_create_row)


def test_put_customer_success(
    customer_put_update: Customer,
    mock_storage: CustomerStorage,
    service: CustomerService,
):
    """
    Test the successful update of a customer using the PUT method.

    Args:
        customer_put_update (Customer): The updated customer data.
        mock_storage (MagicMock): The mocked storage layer.
        service (CustomerService): The CustomerService instance.
    """
    mock_storage.update_customer.return_value = customer_put_update
    result = service.update_customer(customer_put_update)
    assert result.updated_at is not None
    mock_storage.update_customer.assert_called_once_with(customer_put_update)


def test_put_customer_failure(
    customer_put_update: Customer,
    mock_storage: CustomerStorage,
    service: CustomerService,
):
    """
    Test the handling of EntityNotFound when updating a customer with the PUT method.

    Args:
        customer_put_update (Customer): The updated customer data.
        mock_storage (MagicMock): The mocked storage layer.
        service (CustomerService): The CustomerService instance.
    """
    mock_storage.update_customer.side_effect = EntityNotFound("Customer not found")
    with raises(EntityNotFound):
        service.update_customer(customer_put_update)
    mock_storage.update_customer.assert_called_once_with(customer_put_update)


def test_patch_customer_sucess(
    customer_patch_update: CustomerUpdate,
    mock_storage: CustomerStorage,
    service: CustomerService,
):
    """
    Test the successful partial update of a customer using the PATCH method.

    Args:
        customer_patch_update (CustomerUpdate): The partial customer update data.
        mock_storage (MagicMock): The mocked storage layer.
        service (CustomerService): The CustomerService instance.
    """
    mock_storage.patch_customer.return_value = customer_patch_update
    result = service.patch_customer(customer_patch_update)
    assert result.updated_at is not None
    mock_storage.patch_customer.assert_called_once_with(customer_patch_update)


def test_patch_customer_failure(
    customer_patch_update: CustomerUpdate,
    mock_storage: CustomerStorage,
    service: CustomerService,
):
    """
    Test the handling of EntityNotFound when updating a customer with the PATCH method.

    Args:
        customer_patch_update (CustomerUpdate): The partial customer update data.
        mock_storage (MagicMock): The mocked storage layer.
        service (CustomerService): The CustomerService instance.
    """
    mock_storage.patch_customer.side_effect = EntityNotFound("Customer not found")
    with raises(EntityNotFound):
        service.patch_customer(customer_patch_update)
    mock_storage.patch_customer.assert_called_once_with(customer_patch_update)
