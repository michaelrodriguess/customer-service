"""
This module contains test fixtures for the customer service.

The fixtures provide mock objects and data to facilitate testing of the
`CustomerService` and related components, ensuring that test cases are isolated
and do not depend on actual database connections or external systems.
"""

from datetime import datetime
from pytest import fixture
from models.customer_model import Customer, CustomerUpdate


@fixture
def customer():
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
        created_at=datetime(2024, 1, 1, 12, 0, 0),
        updated_at=None,
    )


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
        created_at=datetime(2024, 1, 1, 12, 0, 0),
        updated_at=datetime(2024, 1, 1, 00, 0, 0),
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
        updated_at="2024-01-01T00:00:00",
    )


@fixture
def invalid_customer_update_put():
    """
    Provides a mock `Customer` object with mismatched data for negative test cases.

    Returns:
        Customer: A customer instance with differing email data for PUT tests.
    """
    return Customer(
        id="01F8MECHZX3TBDSZ7XD96VR2H5", name="John Doe", email="test@test.com"
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


@fixture
def put_tuple():
    return (
        "01F8MECHZX3TBDSZ7XD96VR2H5",
        "John Doe",
        "johndoe@example.com",
        True,
        datetime(2024, 1, 1, 12, 0, 0),
        None,
    )


@fixture
def patch_tuple():
    return (
        "01F8MECHZX3TBDSZ7XD96VR2H5",
        "John Doe",
        "johndoe@example.com",
        False,
        datetime(2024, 1, 1, 0, 0, 0),
    )
