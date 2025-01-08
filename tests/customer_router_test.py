import pytest
from unittest.mock import MagicMock
from routes import customer_router
from fastapi.testclient import TestClient


@pytest.fixture
def router():
    mock_service = MagicMock()
