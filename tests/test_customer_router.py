import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app
from routes.customer_router import get_customer_service
import datetime
from exceptions.customer_exceptions import EntityNotFound


@pytest.fixture
def mock_service(service, customer_put_update, customer_patch_update):
    service.update_customer = MagicMock(return_value=customer_put_update)
    service.patch_customer = MagicMock(return_value=customer_patch_update)
    return service


@pytest.fixture
def appTest(mock_service):
    app.dependency_overrides[get_customer_service] = lambda: mock_service
    return TestClient(app)


@pytest.fixture
def customer_put_update_json():
    return {
        "id": "01F8MECHZX3TBDSZ7XD96VR2H5",
        "name": "John Doe",
        "email": "johndoe@example.com",
        "active": True,
        "created_at": "2020-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00",
    }


@pytest.fixture
def customer_patch_update_json():
    return {
        "id": "01F8MECHZX3TBDSZ7XD96VR2H5",
        "name": "John Doe",
        "email": "johndoe@example.com",
        "active": False,
        "updated_at": "2024-01-01T00:00:00",
    }


def test_put_customer_success(appTest, customer_put_update_json):
    response = appTest.put(
        "/customers/",
        json={
            "id": "01F8MECHZX3TBDSZ7XD96VR2H5",
            "name": "John Doe",
            "email": "teste@test.com",
        },
    )
    assert response.status_code == 200
    assert response.json() == customer_put_update_json


def test_patch_customer_sucess(appTest, customer_patch_update_json):
    response = appTest.patch(
        "/customers/",
        json={
            "id": "01F8MECHZX3TBDSZ7XD96VR2H5",
            "name": "John Doe",
            "email": "teste@teste.com",
            "active": False,
        },
    )
    assert response.status_code == 200
    assert response.json() == customer_patch_update_json


def test_put_customer_EntityNotFound(appTest, mock_service):
    mock_service.update_customer.side_effect = EntityNotFound("Customer not found")
    response = appTest.put(
        "/customers/",
        json={
            "id": "01F8MECHZX3TBDSZ7XD96VR2H1",
            "name": "John Doe",
            "email": "teste@teste.com",
        },
    )
    assert response.status_code == 404


def test_patch_customer_EntityNotFound(appTest, mock_service):
    mock_service.patch_customer.side_effect = EntityNotFound("Customer not found")
    response = appTest.patch(
        "/customers/",
        json={
            "id": "01F8MECHZX3TBDSZ7XD96VR2H",
            "name": "John Doe",
            "email": "teste@teste.com",
        },
    )
    assert response.status_code == 404
