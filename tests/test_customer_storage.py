"""
This module contains tests for the CustomerStorage class, simulating database interactions 
using mock objects for the cursor and database connection.
"""

from unittest.mock import MagicMock
import pytest
from psycopg2 import DatabaseError, IntegrityError
from storages.customer_storage import CustomerStorage


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
