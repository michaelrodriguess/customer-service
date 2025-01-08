from pytest import fixture, raises
import datetime
from unittest.mock import MagicMock
from services.customer_service import CustomerService
from models.customer_model import Customer, CustomerUpdate
from storages.customer_storage import CustomerStorage, EntityNotFound


@fixture
def storage():
    mock_db = MagicMock()
    cursor_mock = MagicMock()
    cursor_mock.fetchone.return_value = (
        "01F8MECHZX3TBDSZ7XD96VR2H5",
        "John Doe",
        "johndoe@example.com",
        True,
        datetime.datetime(2020, 1, 1),
        datetime.datetime(2024, 1, 1),
    )
    mock_db.cursor.return_value.__enter__.return_value = cursor_mock
    storage = CustomerStorage(db_connection=mock_db)
    return storage, cursor_mock


@fixture
def customer_put_update():
    return Customer(
        id="01F8MECHZX3TBDSZ7XD96VR2H5",
        name="John Doe",
        email="johndoe@example.com",
        active=True,
        created_at=datetime.datetime(2020, 1, 1),
        updated_at=datetime.datetime(2024, 1, 1),
    )


@fixture
def customer_patch_update():
    return CustomerUpdate(
        id="01F8MECHZX3TBDSZ7XD96VR2H5",
        name="John Doe",
        email="johndoe@example.com",
        active=False,
    )


@fixture
def not_customer_update_put():
    return Customer(
        id="01F8MECHZX3TBDSZ7XD96VR2H5", name="John Doe", email="test@test.com"
    )


@fixture
def mock_storage():
    return MagicMock()


@fixture
def service(mock_storage):
    return CustomerService(storage=mock_storage)
