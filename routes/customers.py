from fastapi import APIRouter, HTTPException
from models.customer import Customer
from services.customer_service import Customer_service

ProductRouter = APIRouter()


@ProductRouter.put("/customers/{id}")
def update_customer(id: int, customer_update: Customer):

    customer_service = Customer_service()
    updated_customer = customer_service.update_customer(id, customer_update)

    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return updated_customer
