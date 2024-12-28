from fastapi import APIRouter, HTTPException
from models.customer_model import Customer, Customer_update
from services.customer_service import Customer_service
from storages.customers_storage import EntityNotFound

customer_service = Customer_service()
CustomerRouter = APIRouter()


@CustomerRouter.put("/customers/", response_model=Customer_update)
def update_customer(customer_update: Customer):
    try:
        return customer_service.update_customer(customer_update)

    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)


@CustomerRouter.patch("/customers/", response_model=Customer_update)
def patch_customer(customer_update: Customer_update):
    try:
        return customer_service.patch_customer(customer_update)

    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
