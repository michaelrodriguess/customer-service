from unittest.mock import MagicMock
from datetime import datetime
from storages.customer_storage import CustomerStorage
from models.customer_model import Customer
import pytest

@pytest.fixture
def customer_row():
    return (
        "01F8MECHZX3TBDSZ7XD96VR2H5",
        "John Doe",
        "johndoe@example.com",
        datetime(2024, 1, 1, 12, 0, 0),
        None,
        True
    )

def test_get_customer_by_id(mock_cursor, storage, customer, customer_row):
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

def test_get_all_customer_success(mock_cursor, storage, customer, customer_row):
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
