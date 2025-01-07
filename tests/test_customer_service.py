import pytest
from unittest.mock import MagicMock
from services.customer_service import CustomerService


@pytest.fixture
def service():
    mock_db = MagicMock()
    service = CustomerService(storage=mock_db)
    return service, mock_db


def test_delete_customer_calls_storage(service):
    service, mock_db = service
    customer_id = "01JGQ1XA2VW0K0WMTTJRXT5SXK"

    service.delete_customer(customer_id)
    mock_db.delete_customer.asser_called_once_with(customer_id)


def test_delete_customer_key_error(service):
    service, mock_db = service
    customer_id = "01JGQ1XA2VW0K0WMTTJRXT5SXK"

    mock_db.delete_customer.side_effect = KeyError("Simulating the KeyError")

    with pytest.raises(KeyError):
        service.delete_customer(customer_id)

    mock_db.delete_customer.assert_called_once()
