from fastapi import APIRouter, HTTPException
from models.customer import Customer, Customer_update
from services.customer_service import Customer_service

CustomerRouter = APIRouter()


@CustomerRouter.put("/customers/{id}")
def update_customer(id: str, customer_update: Customer):

    customer_service = Customer_service()
    updated_customer = customer_service.update_customer(id, customer_update)

    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return updated_customer


@CustomerRouter.patch("/customers/{id}")
def patch_customer(id: str, customer_update: Customer_update):
    customer_service = Customer_service()
    updated_customer = customer_service.patch_customer(id, customer_update)

    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return update_customer
