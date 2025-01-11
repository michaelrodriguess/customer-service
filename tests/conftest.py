from pytest import fixture
from unittest.mock import MagicMock
from services.customer_service import CustomerService
from storages.customer_storage import CustomerStorage
from fastapi.testclient import TestClient
from routes.customer_router import get_customer_service
from main import app


@fixture
def storage():
    mock_db = MagicMock()
    cursor_mock = MagicMock()
    mock_db.cursor.return_value.__enter__.return_value = cursor_mock
    storage = CustomerStorage(db_connection=mock_db)
    return storage, cursor_mock


@fixture
def simple_storage_for_service():
    storage = MagicMock(CustomerStorage)
    return storage


@fixture
def service(simple_storage_for_service):
    service = CustomerService(storage=simple_storage_for_service)
    return service


@fixture
def router():
    mock_service = MagicMock()
    app.dependency_overrides[get_customer_service] = lambda: mock_service
    router = TestClient(app)
    return mock_service, router
