"""
This module contains test fixtures for the customer service.
"""
from pytest import fixture
from unittest.mock import MagicMock
from services.customer_service import CustomerService
from storages.customer_storage import CustomerStorage
from models.customer_model import Customer
from fastapi.testclient import TestClient
from routes.customer_router import get_customer_service
from main import app
from datetime import datetime


@fixture
def storage_for_delete():
    """
    Fixture for mocking database storage and cursor for the delete tests.
    """
    mock_db = MagicMock()
    cursor_mock = MagicMock()
    mock_db.cursor.return_value.__enter__.return_value = cursor_mock
    storage = CustomerStorage(db_connection=mock_db)
    return storage, cursor_mock


@fixture
def simple_storage_for_service():
    """
    Fixture for mocking CustomerStorage instance for service tests.
    """
    storage = MagicMock(CustomerStorage)
    return storage


@fixture
def service(simple_storage_for_service):
    """
    Fixture for creating a mocked CustomerService instance.
    """
    service = CustomerService(storage=simple_storage_for_service)
    return service


@fixture
def router():
    """
    Fixture for creating a mocked service and FastAPI router for testing.
    """
    mock_service = MagicMock()
    app.dependency_overrides[get_customer_service] = lambda: mock_service
    router = TestClient(app)
    return mock_service, router


@fixture
def customer_create_row():
    """
    Fixture to create a Customer instance with dummy data for testing.
    """
    return Customer(
        id="01F8MECHZX3TBDSZ7XD96VR2H5",
        name="John Doe",
        email="johndoe@example.com",
        active=True,
        created_at=datetime(2024, 1, 1, 12, 0, 0),
        updated_at=None,
    )
