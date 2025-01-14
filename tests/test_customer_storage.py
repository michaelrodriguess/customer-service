"""
Tests for CustomerStorage using mock database interactions.
"""

from datetime import datetime
from unittest.mock import MagicMock, ANY
import pytest
from psycopg2 import DatabaseError, IntegrityError, sql
from pytest import fixture, raises
from storages.customer_storage import CustomerStorage
from exceptions.customer_exceptions import EntityNotFound
from models.customer_model import Customer, CustomerUpdate


@fixture(name="cursor")
def fixture_cursor():
    """
    Creates a mock cursor for database interactions.
    """
    return MagicMock()


@fixture(name="db_conn")
def fixture_db_conn(cursor: MagicMock):
    """
    Creates a mock database connection using the provided cursor.
    """
    db_conn = MagicMock()
    db_conn.cursor.return_value.__enter__.return_value = cursor
    return db_conn


@fixture(name="storage")
def fixture_storage(db_conn: MagicMock) -> CustomerStorage:
    """
    Creates a CustomerStorage instance with a mock database connection.
    """
    return CustomerStorage(db_conn)


@fixture(name="customer_row")
def fixture_customer_row():
    """
    Fixture that returns a tuple representing a fictional customer.
    """
    return (
        "01F8MECHZX3TBDSZ7XD96VR2H5",
        "John Doe",
        "johndoe@example.com",
        datetime(2024, 1, 1, 12, 0, 0),
        None,
        True,
    )


def test_get_customer_by_id(cursor, storage, customer, customer_row):
    """
    Test that `get_customer_by_id` retrieves a customer by ID from the database
    and maps the result to the expected customer model.
    """
    cursor.fetchone.return_value = customer_row

    result = storage.get_customer_by_id("01F8MECHZX3TBDSZ7XD96VR2H5")
    assert result == customer

    cursor.execute.assert_called_once_with
    (
        """
        SELECT id, name, email, created_at, updated_at, active
        FROM customers
        WHERE id = %s AND active = true;
        """,
        ("01F8MECHZX3TBDSZ7XD96VR2H5",),
    )


def test_get_customer_by_id_value_error(cursor, storage):
    """
    Test that `get_customer_by_id` raises a `ValueError`
    when the customer with the given ID does not exist in the database.
    """
    cursor.fetchone.return_value = None

    with pytest.raises(ValueError):
        storage.get_customer_by_id("01JFTE35ZRRZWCSKK6TBB1DZCT")

    cursor.execute.assert_called_once()
    cursor.fetchone.assert_called_once()


def test_get_all_customer_success(cursor, storage, customer_create_row, customer_row):
    """
    Test that `get_all_customers` retrieves all active customers from the database
    and maps the results to the expected customer model.
    """
    cursor.fetchall.return_value = [customer_row]

    result = storage.get_all_customers()
    assert result == [customer_create_row]

    cursor.execute.assert_called_once_with
    (
        """
        SELECT id, name, email, created_at, updated_at, active
        FROM customers
        WHERE active = true;
        """
    )


def test_get_all_customers_database_error(cursor, storage):
    """
    Test that `get_all_customers` raises a `DatabaseError`
    when an error occurs during query execution.
    """
    cursor.execute.side_effect = DatabaseError()

    with pytest.raises(DatabaseError):
        storage.get_all_customers()

    cursor.execute.assert_called_once()
    cursor.fetchall.assert_not_called()


def test_create_customer_success(cursor, storage, customer):
    """
    Test the successful creation of a customer.
    """
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


def test_create_customer_integrity_error(storage, cursor, customer):
    """
    Test handling of IntegrityError when creating a customer.
    """
    cursor.execute.side_effect = IntegrityError()

    with raises(IntegrityError):
        storage.create_customer(customer)

    storage.db.rollback.assert_called_once()
    storage.db.commit.assert_not_called()


def test_create_customer_database_error(storage, cursor, customer):
    """
    Test handling of DatabaseError when creating a customer.
    """
    cursor.execute.side_effect = DatabaseError()

    with raises(DatabaseError):
        storage.create_customer(customer)

    storage.db.rollback.assert_called_once()
    storage.db.commit.assert_not_called()


def test_put_customer_success(cursor, storage: CustomerStorage, customer: Customer):
    """
    Test the successful update of a customer.

    Verifies that the customer data is correctly updated in the storage layer.

    Args:
        cursor (MagicMock): The mock cursor object.
        storage (CustomerStorage): The storage instance.
        customer_put_update (Customer): The customer data to update.
    """
    cursor.fetchone.return_value = (
        customer.id,
        customer.name,
        customer.email,
        customer.active,
        customer.created_at,
        customer.updated_at,
    )

    updated_customer = storage.update_customer(customer)

    assert updated_customer == customer
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
            customer.name,
            customer.email,
            ANY,
            customer.id,
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
    cursor, storage: CustomerStorage, customer: Customer
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
        storage.update_customer(customer)


def test_put_customer_database_error(
    cursor, storage: CustomerStorage, customer: Customer
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
        storage.update_customer(customer)


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
        customer_patch_update (CustomerUpdate): Partial customer data to patch update.
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


def test_delete_customer(storage, cursor):
    """
    Tests customer deletion by verifying the deactivation query execution.
    """
    customer_id = "01JGQ1XA2VW0K0WMTTJRXT5SXK"
    cursor.rowcount = 1

    storage.delete_customer(customer_id)
    cursor.execute.assert_called_once_with(
        """
                    UPDATE customers
                    SET active = FALSE, updated_at = NOW()
                    WHERE id = %s AND active = TRUE;
                    """,
        (customer_id,),
    )
    storage.db.commit.assert_called_once()


def test_delete_customer_not_found(storage, cursor):
    """
    Tests failure of customer deletion when not found or inactive.
    """
    customer_id = "01JGQ1XA2VW0K0WMTTJRXT5SXK"
    cursor.rowcount = 0

    with raises(
        KeyError, match=f"Customer id={customer_id} not found or already inactive."
    ):
        storage.delete_customer(customer_id)

    cursor.execute.assert_called_once_with(
        """
                    UPDATE customers
                    SET active = FALSE, updated_at = NOW()
                    WHERE id = %s AND active = TRUE;
                    """,
        (customer_id,),
    )


def test_delete_customer_database_error(storage, cursor):
    """
    Tests handling of database error during customer deletion.
    """
    customer_id = "01JGQ1XA2VW0K0WMTTJRXT5SXK"

    cursor.execute.side_effect = DatabaseError()

    with raises(DatabaseError):
        storage.delete_customer(customer_id)

    storage.db.rollback.assert_called_once()
