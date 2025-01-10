from datetime import datetime
from unittest.mock import MagicMock

from pytest import fixture

from models.customer_model import Customer


@fixture(name="mock_cursor")
def fixture_mock_cursor():
    """
    This mock simulates the behavior of a database cursor, allowing controlled testing
    of database interactions without connecting to an actual database.
    """
    return MagicMock()


@fixture(name="mock_db")
def fixture_mock_db(mock_cursor):
    """
    The mock database connection returns a mocked cursor when the `cursor()` method
    is called. This allows testing database-dependent components in isolation.
    """
    mock_db = MagicMock()
    mock_db.cursor.return_value.__enter__.return_value = mock_cursor
    return mock_db


@fixture
def customer():
    """
    The instance represents a fictional customer and can be used in tests
    to verify the behavior of components that interact with customer data.
    """
    return Customer(
        id="01F8MECHZX3TBDSZ7XD96VR2H5",
        name="John Doe",
        email="johndoe@example.com",
        active=True,
        created_at=datetime(2024, 1, 1, 12, 0, 0),
        updated_at=None,
    )
