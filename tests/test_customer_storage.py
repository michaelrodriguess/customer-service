from pytest import fixture
from datetime import datetime
from unittest.mock import MagicMock
from models.customer_model import Customer
# from psycopg2 import DatabaseError, IntegrityError
from storages.customer_storage import CustomerStorage


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
def storage(mock_db):
    """
    This enables testing of the `CustomerStorage` class without requiring a real database,
    ensuring controlled and predictable behavior during tests.
    """
    return CustomerStorage(mock_db)


def test_create_customer_success(mock_cursor, storage, customer_create_row):
    #arrange
    customer = customer_create_row
    result = storage.create_customer(customer)

    #assert que o cliente retornado é o esperado
    assert result == customer

    #assert que a query foi chamada corretamente
    mock_cursor.execute.assert_called_once_with(
    """
                    INSERT INTO customers (id, name, email, created_at, active)
                    VALUES (%s, %s, %s, NOW(), TRUE);
                    """,
    (customer.id, customer.name, customer.email),
)


    #assert que o commit foi chamado.
    storage.db.commit.assert_called_once()



# def test_create_customer_integrity_error(storage, mock_cursor, customer_row):
#     mock_cursor.execute.side_effect = IntegrityError()
#     customer = Customer(*customer_row[:3])

#     with pytest.raises(IntegrityError):
#         storage.create_customer(customer)

#     # Assert que o rollback foi chamado
#     storage.db.rollback.assert_called_once()

#     # Assert que o commit NÃO foi chamado
#     storage.db.commit.assert_not_called()

    

# def test_create_customer_database_error(storage, mock_cursor, customer_row):
#     mock_cursor.execute.side_effect = DatabaseError()
#     customer = Customer(*customer_row[:3])

#     with pytest.raises(DatabaseError):
#         storage.create_customer(customer)

#     # Assert que o rollback foi chamado
#     storage.db.rollback.assert_called_once()
#     storage.db.commit.assert_not_called()
