from unittest.mock import MagicMock
import pytest
from services.customer_service import CustomerService
from storages.customer_storage import CustomerStorage, EntityNotFound
from models.customer_model import Customer, CustomerUpdate


def test_put_customer_success(
    customer_put_update: Customer,
    mock_storage: CustomerStorage,
    service: CustomerService,
):
    mock_storage.update_customer.return_value = customer_put_update
    result = service.update_customer(customer_put_update)
    assert result.updated_at is not None
    mock_storage.update_customer.assert_called_once_with(customer_put_update)


def test_put_customer_failure(
    customer_put_update: Customer,
    mock_storage: CustomerStorage,
    service: CustomerService,
):
    mock_storage.update_customer.side_effect = EntityNotFound("Customer not found")
    with pytest.raises(EntityNotFound):
        service.update_customer(customer_put_update)
    mock_storage.update_customer.assert_called_once_with(customer_put_update)


def test_patch_customer_sucess(
    customer_patch_update: CustomerUpdate,
    mock_storage: CustomerStorage,
    service: CustomerService,
):
    mock_storage.patch_customer.return_value = customer_patch_update
    result = service.patch_customer(customer_patch_update)
    assert result.updated_at is not None
    mock_storage.patch_customer.assert_called_once_with(customer_patch_update)


def test_patch_customer_failure(
    customer_patch_update: CustomerUpdate,
    mock_storage: CustomerStorage,
    service: CustomerService,
):
    mock_storage.patch_customer.side_effect = EntityNotFound("Customer not found")
    with pytest.raises(EntityNotFound):
        service.patch_customer(customer_patch_update)
    mock_storage.patch_customer.assert_called_once_with(customer_patch_update)
