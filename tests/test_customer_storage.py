"""
Tests for CustomerStorage using mock database interactions.
"""
from unittest.mock import MagicMock
from pytest import fixture, raises
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
                    (customer.id, customer.name, customer.email),)

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
        KeyError,
            match=f"Customer id={customer_id} not found or already inactive."):
        storage.delete_customer(customer_id)

    cursor.execute.assert_called_once_with(
                    """
                    UPDATE customers
                    SET active = FALSE, updated_at = NOW()
                    WHERE id = %s AND active = TRUE;
                    """,
                    (customer_id,),)


def test_delete_customer_database_error(storage, cursor):
    """
    Tests handling of database error during customer deletion.
    """
    customer_id = "01JGQ1XA2VW0K0WMTTJRXT5SXK"

    cursor.execute.side_effect = DatabaseError()

    with raises(DatabaseError):
        storage.delete_customer(customer_id)

    storage.db.rollback.assert_called_once()
