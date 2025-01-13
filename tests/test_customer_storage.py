"""
This module contains tests for the CustomerStorage class, simulating database interactions
using mock objects for the cursor and database connection.
"""

from unittest.mock import MagicMock, ANY
import pytest
from psycopg2 import DatabaseError, IntegrityError, sql
from storages.customer_storage import CustomerStorage
from pytest import raises
from exceptions.customer_exceptions import EntityNotFound
from models.customer_model import Customer, CustomerUpdate


@pytest.fixture(name="cursor")
def fixture_cursor():
    """
    Creates a mock cursor object to simulate database interactions.
    Returns:
        MagicMock: A mock cursor object.
    """
    return MagicMock()


@pytest.fixture(name="db_conn")
def fixture_db_conn(cursor: MagicMock):
    """
    Creates a mock database connection object with a mock cursor.
    Args:
        cursor (MagicMock): A mock cursor object.
    Returns:
        MagicMock: A mock database connection object.
    """
    db_conn = MagicMock()
    db_conn.cursor.return_value.__enter__.return_value = cursor
    return db_conn


@pytest.fixture(name="storage")
def fixture_storage(db_conn: MagicMock) -> CustomerStorage:
    """
    Creates an instance of CustomerStorage with a mock database connection.
    Args:
        db_conn (MagicMock): A mock database connection object.
    Returns:
        CustomerStorage: A storage instance using the mock database connection.
    """
    return CustomerStorage(db_conn)


def test_create_customer_success(cursor, storage, customer_create_row):
    """
    Test the successful creation of a customer.
    """
    customer = customer_create_row
    result = storage.create_customer(customer)

    assert result == customer

    cursor.execute.assert_called_once_with(
        """
                    INSERT INTO customers (id, name, email, created_at, active)
                    VALUES (%s, %s, %s, NOW(), TRUE);
                    """,
        (customer.id, customer.name, customer.email),
    )

    storage.db.commit.assert_called_once()


def test_create_customer_integrity_error(storage, cursor, customer_create_row):
    """
    Test handling of IntegrityError when creating a customer.
    """
    cursor.execute.side_effect = IntegrityError()
    customer = customer_create_row

    with pytest.raises(IntegrityError):
        storage.create_customer(customer)

    storage.db.rollback.assert_called_once()
    storage.db.commit.assert_not_called()


def test_create_customer_database_error(storage, cursor, customer_create_row):
    """
    Test handling of DatabaseError when creating a customer.
    """
    cursor.execute.side_effect = DatabaseError()
    customer = customer_create_row

    with pytest.raises(DatabaseError):
        storage.create_customer(customer)

    storage.db.rollback.assert_called_once()
    storage.db.commit.assert_not_called()


def test_put_customer_success(
    cursor, storage: CustomerStorage, customer_put_update: Customer
):
    """
    Test the successful update of a customer.

    Verifies that the customer data is correctly updated in the storage layer.

    Args:
        cursor (MagicMock): The mock cursor object.
        storage (CustomerStorage): The storage instance.
        customer_put_update (Customer): The customer data to update.
    """
    cursor.fetchone.return_value = (
        customer_put_update.id,
        customer_put_update.name,
        customer_put_update.email,
        customer_put_update.active,
        customer_put_update.created_at,
        customer_put_update.updated_at,
    )

    updated_customer = storage.update_customer(customer_put_update)

    assert updated_customer == customer_put_update
    storage.db.commit.assert_called_once()
    cursor.execute.assert_called_once_with(
        sql.SQL(
            """
                    UPDATE customers
                    SET name = %s, email = %s, updated_at = %s
                    WHERE id = %s AND active = true
                    RETURNING id, name, email, active, created_at,updated_at;
                    """
        ),
        (
            customer_put_update.name,
            customer_put_update.email,
            ANY,
            customer_put_update.id,
        ),
    )


def test_put_customer_not_exist(
    cursor, storage: CustomerStorage, not_customer_update_put: Customer
):
    """
    Test handling of EntityNotFound when updating a non-existent customer.

    Args:
        cursor (MagicMock): The mock cursor object.
        storage (CustomerStorage): The storage instance.
        not_customer_update_put (Customer): The non-existent customer data.
    """
    cursor.fetchone.return_value = None

    with raises(
        EntityNotFound, match=f"Customer with id {not_customer_update_put.id} not found"
    ):
        storage.update_customer(not_customer_update_put)


def test_put_customer_integrity_error(
    cursor, storage: CustomerStorage, customer_put_update: Customer
):
    """
    Test handling of IntegrityError during customer update.

    Args:
        cursor (MagicMock): The mock cursor object.
        storage (CustomerStorage): The storage instance.
        customer_put_update (Customer): The customer data to update.
    """
    cursor.execute.side_effect = IntegrityError()

    with raises(IntegrityError):
        storage.update_customer(customer_put_update)


def test_put_customer_database_error(
    cursor, storage: CustomerStorage, customer_put_update: Customer
):
    """
    Test handling of DatabaseError during customer update.

    Args:
        cursor (MagicMock): The mock cursor object.
        storage (CustomerStorage): The storage instance.
        customer_put_update (Customer): The customer data to update.
    """
    cursor.execute.side_effect = DatabaseError()

    with raises(DatabaseError):
        storage.update_customer(customer_put_update)


def test_patch_customer_sucess(
    cursor, storage: CustomerStorage, customer_patch_update: CustomerUpdate
):
    """
    Test the successful partial update of a customer.

    Verifies that partial customer data updates are correctly handled.

    Args:
        cursor (MagicMock): The mock cursor object.
        storage (CustomerStorage): The storage instance.
        customer_patch_update (CustomerUpdate): Partial customer data to update.
    """
    cursor.fetchone.return_value = (
        customer_patch_update.id,
        customer_patch_update.name,
        customer_patch_update.email,
        customer_patch_update.active,
        customer_patch_update.updated_at,
    )

    update_customer = storage.patch_customer(customer_patch_update)

    assert update_customer == customer_patch_update
    storage.db.commit.assert_called_once()
    cursor.execute.assert_called_once_with(
        """
                    UPDATE customers
                    SET name = %s, email = %s, active = %s, updated_at = %s
                    WHERE id = %s
                    RETURNING id, name, email, active, updated_at;
                    """,
        (
            [
                customer_patch_update.name,
                customer_patch_update.email,
                customer_patch_update.active,
                customer_patch_update.updated_at,
                customer_patch_update.id,
            ]
        ),
    )


def test_patch_customer_not_exist(
    cursor, storage: CustomerStorage, customer_patch_update: CustomerUpdate
):
    """
    Test handling of EntityNotFound during partial update of a non-existent customer.

    Args:
        cursor (MagicMock): The mock cursor object.
        storage (CustomerStorage): The storage instance.
        customer_patch_update (CustomerUpdate): Partial customer data to update.
    """
    cursor.fetchone.return_value = None

    with raises(
        EntityNotFound, match=f"Customer with id {customer_patch_update.id} not found"
    ):
        storage.patch_customer(customer_patch_update)


def test_patch_customer_integrity_error(
    cursor, storage: CustomerStorage, customer_patch_update: CustomerUpdate
):
    """
    Test handling of IntegrityError during partial customer update.

    Args:
        cursor (MagicMock): The mock cursor object.
        storage (CustomerStorage): The storage instance.
        customer_patch_update (CustomerUpdate): Partial customer data to update.
    """
    cursor.execute.side_effect = IntegrityError()

    with raises(IntegrityError):
        storage.patch_customer(customer_patch_update)


def test_patch_customer_database_error(
    cursor, storage: CustomerStorage, customer_patch_update: CustomerUpdate
):
    """
    Test handling of DatabaseError during partial customer update.

    Args:
        cursor (MagicMock): The mock cursor object.
        storage (CustomerStorage): The storage instance.
        customer_patch_update (CustomerUpdate): Partial customer data to update.
    """
    cursor.execute.side_effect = DatabaseError()

    with raises(DatabaseError):
        storage.patch_customer(customer_patch_update)
