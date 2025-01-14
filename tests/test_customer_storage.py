"""
Tests for CustomerStorage using mock database interactions.
"""

from unittest.mock import MagicMock
import pytest
from pytest import fixture, raises
from datetime import datetime
from psycopg2 import DatabaseError, IntegrityError
from storages.customer_storage import CustomerStorage


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


def test_get_all_customer_success(cursor, storage, customer, customer_row):
    """
    Test that `get_all_customers` retrieves all active customers from the database
    and maps the results to the expected customer model.
    """
    cursor.fetchall.return_value = [customer_row]

    result = storage.get_all_customers()
    assert result == [customer]

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


def test_get_customer_by_email(storage, cursor, customer, customer_row):
    """
    Tests if get retrives a customer by email from database.
    """
    customer_email = "johndoe@example.com"
    cursor.fetchone.return_value = customer_row

    result = storage.get_customer_by_email(customer_email)
    assert result == customer

    cursor.execute.assert_called_once_with(
                    """
                    SELECT id, name, email, created_at, updated_at, active
                    FROM customers
                    WHERE email = %s AND active = true;
                    """,
                    (customer_email,),
    )


def test_get_customer_by_email_not_found(cursor, storage):
    """
    Tests if the customer does not exist in the database.
    """
    customer_email = "johndoe@example.com"
    cursor.fetchone.return_value = None

    with raises(ValueError):
        storage.get_customer_by_email(customer_email)

    cursor.execute.assert_called_once()
    cursor.fetchone.assert_called_once()


def test_get_customer_by_email_database_error(cursor, storage):
    """
    Tests the case of having a database error.
    """
    customer_email = "johndoe@example.com"
    cursor.execute.side_effect = DatabaseError()

    with raises(DatabaseError):
        storage.get_customer_by_email(customer_email)

    cursor.execute.assert_called_once()
    cursor.fetchall.ssert_not_called()
