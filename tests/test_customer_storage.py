import pytest
from unittest.mock import MagicMock
from storages.customer_storage import CustomerStorage
from psycopg2 import DatabaseError


@pytest.fixture
def storage():
    mock_db = MagicMock()
    cursor_mock = MagicMock()
    mock_db.cursor.return_value.__enter__.return_value = cursor_mock
    storage = CustomerStorage(db_connection=mock_db)
    return storage, cursor_mock


def test_delete_customer(storage):
    storage, cursor_mock = storage
    customer_id = "01JGQ1XA2VW0K0WMTTJRXT5SXK"
    cursor_mock.rowcount = 1

    storage.delete_customer(customer_id)
    cursor_mock.execute.assert_called_once_with(
                    """
                    UPDATE customers
                    SET active = FALSE, updated_at = NOW()
                    WHERE id = %s AND active = TRUE;
                    """,
                    (customer_id,),
        )
    storage.db.commit.assert_called_once()


def test_delete_customer_not_found(storage):
    storage, cursor_mock = storage
    customer_id = "01JGQ1XA2VW0K0WMTTJRXT5SXK"
    cursor_mock.rowcount = 0

    with pytest.raises(KeyError, match=f"Customer id={customer_id} not found or already inactive."):
        storage.delete_customer(customer_id)

    cursor_mock.execute.assert_called_once_with(
                    """
                    UPDATE customers
                    SET active = FALSE, updated_at = NOW()
                    WHERE id = %s AND active = TRUE;
                    """,
                    (customer_id,),
        )


def test_delete_customer_database_error(storage):
    storage, cursor_mock = storage
    customer_id = "01JGQ1XA2VW0K0WMTTJRXT5SXK"

    cursor_mock.execute.side_effect = DatabaseError()

    with pytest.raises(DatabaseError):
        storage.delete_customer(customer_id)
        storage.db.rollback.assert_called_once()
