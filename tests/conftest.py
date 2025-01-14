"""
This module contains test fixtures for the customer service.

The fixtures provide mock objects and data to facilitate testing of the
`CustomerService` and related components, ensuring that test cases are isolated
and do not depend on actual database connections or external systems.
"""

from pytest import fixture
import datetime
from models.customer_model import Customer, CustomerUpdate


@fixture
def customer_put_update():
    """
    Provides a mock `Customer` object representing a full update scenario.

    Returns:
        Customer: A customer instance with dummy data for PUT operations.
    """
    return Customer(
        id="01F8MECHZX3TBDSZ7XD96VR2H5",
        name="John Doe",
        email="johndoe@example.com",
        active=True,
        created_at="2020-01-01T00:00:00",
        updated_at="2024-01-01T00:00:00",
    )


@fixture
def customer_patch_update():
    """
    Provides a mock `CustomerUpdate` object representing a partial update scenario.

    Returns:
        CustomerUpdate: A customer update instance with dummy data for PATCH operations.
    """
    return CustomerUpdate(
        id="01F8MECHZX3TBDSZ7XD96VR2H5",
        name="John Doe",
        email="johndoe@example.com",
        active=False,
        updated_at=datetime.datetime(2024, 1, 1, 0, 0),
    )


@fixture
def not_customer_update_put():
    """
    Provides a mock `Customer` object with mismatched data for negative test cases.

    Returns:
        Customer: A customer instance with differing email data for PUT tests.
    """
    return Customer(
        id="01F8MECHZX3TBDSZ7XD96VR2H5", name="John Doe", email="test@test.com"
    )


@fixture
def customer_create_row():
    """
    Provides a mock `Customer` object representing a new customer row for testing.

    Returns:
        Customer: A customer instance with dummy data for insertion tests.
    """
    return Customer(
        id="01F8MECHZX3TBDSZ7XD96VR2H5",
        name="John Doe",
        email="johndoe@example.com",
        active=True,
        created_at=datetime.datetime(2024, 1, 1, 12, 0, 0),
        updated_at=None,
    )
