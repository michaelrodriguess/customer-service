from pytest import fixture
from datetime import datetime
from models.customer_model import Customer


@fixture
def customer_create_row():
    return Customer(
        id="01JFTE35ZRRZWCSKK6TBB1DZCT",
        name="Joaozin",
        email="joao-da-660@gmail.com",
        created_at=datetime(2024, 12, 23, 15, 57, 25, 496623),
        updated_at=None,
        active=True,
        
    )