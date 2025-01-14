"""
This module contains test fixtures for the customer service.
"""
from datetime import datetime
from unittest.mock import MagicMock

from pytest import fixture

from models.customer_model import Customer

@fixture
def customer():
    """
    Fixture to create a Customer instance with dummy data for testing.
    """
    return Customer(
        id="01F8MECHZX3TBDSZ7XD96VR2H5",
        name="John Doe",
        email="johndoe@example.com",
        active=True,
        created_at=datetime(2024, 1, 1, 12, 0, 0),
        updated_at=None,
    )


@fixture
def customer_row():
    """
    Fixture to create a tuple for the test return.
    """
    return (
        "01F8MECHZX3TBDSZ7XD96VR2H5",
        "John Doe",
        "johndoe@example.com",
        datetime(2024, 1, 1, 12, 0, 0),
        None,
        True,
    )
