"""
Esse módulo faz testes em cima da Service
"""

from unittest.mock import MagicMock
from pytest import raises
import datetime
from storages.customer_storage import CustomerStorage
from exceptions.customer_exceptions import EntityNotFound
from psycopg2 import IntegrityError, DatabaseError
from models.customer_model import Customer, CustomerUpdate


def test_put_customer_success(storage: CustomerStorage, customer_put_update: Customer):
    storage, cursor_mock = storage

    updated_customer = storage.update_customer(customer_put_update)

    assert updated_customer == customer_put_update


def test_put_customer_not_exist(
    storage: CustomerStorage, not_customer_update_put: Customer
):
    storage, cursor_mock = storage

    cursor_mock.fetchone.return_value = None

    with raises(
        EntityNotFound, match=f"Customer with id {not_customer_update_put.id} not found"
    ):
        storage.update_customer(not_customer_update_put)


def test_put_customer_integrity_error(
    storage: CustomerStorage, customer_put_update: Customer
):
    storage, cursor_mock = storage
    cursor_mock.execute.side_effect = IntegrityError()

    with raises(IntegrityError):
        storage.update_customer(customer_put_update)


def test_put_customer_database_error(
    storage: CustomerStorage, customer_put_update: Customer
):
    storage, cursor_mock = storage
    cursor_mock.execute.side_effect = DatabaseError()

    with raises(DatabaseError):
        storage.update_customer(customer_put_update)


def test_patch_customer_sucess(
    storage: CustomerStorage, customer_patch_update: CustomerUpdate
):
    storage, mock_cursor = storage

    update_customer = storage.patch_customer(customer_patch_update)

    assert update_customer.id == customer_patch_update.id


def test_patch_customer_not_exist(
    storage: CustomerStorage, customer_patch_update: CustomerUpdate
):
    storage, cursor_mock = storage
    cursor_mock.fetchone.return_value = None

    with raises(
        EntityNotFound, match=f"Customer with id {customer_patch_update.id} not found"
    ):
        storage.update_customer(customer_patch_update)


def test_patch_customer_integrity_error(
    storage: CustomerStorage, customer_patch_update: Customer
):
    storage, cursor_mock = storage
    cursor_mock.execute.side_effect = IntegrityError()

    with raises(IntegrityError):
        storage.update_customer(customer_patch_update)


def test_patch_customer_database_error(
    storage: CustomerStorage, customer_patch_update: Customer
):
    storage, cursor_mock = storage
    cursor_mock.execute.side_effect = DatabaseError()

    with raises(DatabaseError):
        storage.update_customer(customer_patch_update)


"""
está rolando uns falsos positivos, já que não dei o assert pra validar o que esses de db estão retornando
"""
