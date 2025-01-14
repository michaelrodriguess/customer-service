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


def test_get_customer_by_id_successfully(customer, mock_storage, service):
    """
    Tests that the `get_customer_by_id` method retrieves the correct customer
    when a valid customer ID is provided.
    """
    mock_storage.get_customer_by_id.return_value = customer

    result = service.get_customer_by_id("01F8MECHZX3TBDSZ7XD96VR2H5")
    assert result == customer
    mock_storage.get_customer_by_id.assert_called_once_with(
        "01F8MECHZX3TBDSZ7XD96VR2H5"
    )


def test_get_customer_by_id_handles_value_error(mock_storage, service):
    """
    Tests that the `get_customer_by_id` method raises a `ValueError`
    when provided with an invalid customer ID.
    """
    mock_storage.get_customer_by_id.side_effect = ValueError()

    with raises(ValueError):
        service.get_customer_by_id("01F8MECHZX3TBDSZ7XD96VR2H0")

    mock_storage.get_customer_by_id.assert_called_once_with(
        "01F8MECHZX3TBDSZ7XD96VR2H0"
    )


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

    with raises(DatabaseError):
        service.get_all_customers()

    mock_storage.get_all_customers.assert_called_once()


def test_create_customer_success(customer, mock_storage, service):
    """
    Test the successful creation of a customer in the service layer.

    Verifies that the service correctly interacts with the storage layer
    to create a customer and returns the expected result.

    Args:
        customer_create_row (dict): The input data for creating a customer.
        mock_storage (MagicMock): The mocked storage layer.
        service (CustomerService): The CustomerService instance.
    """
    mock_storage.create_customer.return_value = customer

    result = service.create_customer(customer)
    assert result == customer
    mock_storage.create_customer.assert_called_once_with(customer)


def test_create_customer_integrity_error(customer_create_row, mock_storage, service):
    """
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
    Verifies that the service raises DatabaseError and interacts with
    the storage layer as expected.

    Args:
        customer_create_row (dict): The input data for creating a customer.
        mock_storage (MagicMock): The mocked storage layer.
        service (CustomerService): The CustomerService instance.
    Test the DatabaseError when creating a customer in the service layer.
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
    customer: Customer,
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
        service.update_customer(customer)
    mock_storage.update_customer.assert_called_once_with(customer)


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

    service.storage.delete_customer.side_effect = KeyError("Simulating the KeyError")

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
