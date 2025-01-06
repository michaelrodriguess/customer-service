from datetime import datetime
from unittest.mock import MagicMock

from pytest import fixture

from models.customer_model import Customer
from storages.customer_storage import CustomerStorage


@fixture
def mock_cursor():
    return MagicMock()


@fixture
def mock_db(mock_cursor):
    mock_db = MagicMock()
    mock_db.cursor.return_value.__enter__.return_value = mock_cursor
    return mock_db


@fixture
def storage(mock_db):
    return CustomerStorage(mock_db)


@fixture
def customer():
    return Customer(
        id="01F8MECHZX3TBDSZ7XD96VR2H5",
        name="John Doe",
        email="johndoe@example.com",
        active=True,
        created_at=datetime(2024, 1, 1, 12, 0, 0),
        updated_at=None,
    )