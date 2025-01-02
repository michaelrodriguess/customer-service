import unittest
from unittest.mock import MagicMock
from datetime import datetime
from storages.customer_storage import CustomerStorage
from models.customer_model import Customer

def test_get_customer_by_id():
    mock_db = MagicMock()
    mock_cursor = MagicMock()
    mock_db.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = ("01F8MECHZX3TBDSZ7XD96VR2H5", "John Doe", "johndoe@example.com", datetime(2024, 1, 1, 12, 0, 0), None, True)
    
    mock_storage = CustomerStorage(mock_db)

    result = mock_storage.get_customer_by_id("01F8MECHZX3TBDSZ7XD96VR2H5")

    assert isinstance(result, Customer)
    assert result.id == "01F8MECHZX3TBDSZ7XD96VR2H5"
    assert result.name == "John Doe"
    assert result.email == "johndoe@example.com"
    assert result.created_at.strftime('%Y-%m-%d %H:%M:%S') == '2024-01-01 12:00:00'
    assert result.updated_at is None
        
def test_get_all_customer_success():
    mock_db = MagicMock()
    mock_cursor = MagicMock()
    mock_db.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        ("01F8MECHZX3TBDSZ7XD96VR2H5", "John Doe", "johndoe@example.com", datetime(2024, 1, 1, 12, 0, 0), None, True),
        ("01F8MECHZX3TBDSZ7XD96VR2H6", "Jane Smith", "janesmith@example.com", datetime(2024, 1, 2, 12, 0, 0), datetime(2024, 1, 1, 12, 0, 0), True)
    ]

    mock_storage = CustomerStorage(mock_db)

    result = mock_storage.get_all_customers()

    assert len(result) == 2
    assert isinstance(result[0], Customer)
    assert isinstance(result[1], Customer)

    assert result[0].id == "01F8MECHZX3TBDSZ7XD96VR2H5"
    assert result[1].id == "01F8MECHZX3TBDSZ7XD96VR2H6"

    assert result[0].name == "John Doe"
    assert result[1].name == "Jane Smith"

    assert result[0].email == "johndoe@example.com"
    assert result[1].email == "janesmith@example.com"

    assert result[0].created_at.strftime("%Y-%m-%d %H:%M:%S") == "2024-01-01 12:00:00"
    assert result[1].created_at.strftime("%Y-%m-%d %H:%M:%S") == "2024-01-02 12:00:00"

    assert result[0].updated_at is None
    assert result[1].updated_at.strftime("%Y-%m-%d %H:%M:%S") == "2024-01-01 12:00:00"
