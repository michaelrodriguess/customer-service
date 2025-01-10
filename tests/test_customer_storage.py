import pytest
from datetime import datetime
from psycopg2 import DatabaseError
from storages.customer_storage import CustomerStorage


@pytest.fixture(name="storage")
def fixture_storage(mock_db):
    """
    This enables testing of the `CustomerStorage` class without requiring a real database,
    ensuring controlled and predictable behavior during tests.
    """
    return CustomerStorage(mock_db)

@pytest.fixture(name="customer_row")
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


def test_get_customer_by_id(mock_cursor, storage, customer, customer_row):
    """
    Test that `get_customer_by_id` retrieves a customer by ID from the database
    and maps the result to the expected customer model.
    """
    mock_cursor.fetchone.return_value = customer_row

    result = storage.get_customer_by_id("01F8MECHZX3TBDSZ7XD96VR2H5")
    assert result == customer

    mock_cursor.execute.assert_called_once_with
    (
        """
        SELECT id, name, email, created_at, updated_at, active
        FROM customers
        WHERE id = %s AND active = true;
        """,
        ("01F8MECHZX3TBDSZ7XD96VR2H5",),
    )


def test_get_customer_by_id_value_error(mock_cursor, storage):
    """
    Test that `get_customer_by_id` raises a `ValueError`
    when the customer with the given ID does not exist in the database.
    """
    mock_cursor.fetchone.return_value = None

    with pytest.raises(ValueError):
        storage.get_customer_by_id("01JFTE35ZRRZWCSKK6TBB1DZCT")

    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchone.assert_called_once()


def test_get_all_customer_success(mock_cursor, storage, customer, customer_row):
    """
    Test that `get_all_customers` retrieves all active customers from the database
    and maps the results to the expected customer model.
    """
    mock_cursor.fetchall.return_value = [customer_row]

    result = storage.get_all_customers()
    assert result == [customer]

    mock_cursor.execute.assert_called_once_with
    (
        """
        SELECT id, name, email, created_at, updated_at, active
        FROM customers
        WHERE active = true;
        """
    )


def test_get_all_customers_database_error(mock_cursor, storage):
    """
    Test that `get_all_customers` raises a `DatabaseError`
    when an error occurs during query execution.
    """
    mock_cursor.execute.side_effect = DatabaseError()

    with pytest.raises(DatabaseError):
        storage.get_all_customers()

    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchall.assert_not_called()
