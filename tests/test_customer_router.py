import pytest
from unittest.mock import MagicMock
from main import app
from fastapi.testclient import TestClient
from routes.customer_router import get_customer_service


@pytest.fixture
def router():
    mock_service = MagicMock()
    app.dependency_overrides[get_customer_service] = lambda: mock_service
    router = TestClient(app)
    return mock_service, router


def test_route_delete_customer(router):
    mock_service, client = router
    customer_id = "01JGQ1XA2VW0K0WMTTJRXT5SXK"

    mock_service.delete_customer.return_value = None
    response = client.delete(f"/customers/{customer_id}")

    assert response.status_code == 204
    mock_service.delete_customer.assert_called_once_with(customer_id)
