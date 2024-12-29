import logging
from fastapi import APIRouter, HTTPException, Response
from services.customer_service import Customer_service
from models.customer_model import Customer, Customer_update
from psycopg2 import DatabaseError
from exceptions.customer_exceptions import EntityNotFound

customer_router = APIRouter()
logger = logging.getLogger(__name__)
customer_service = Customer_service()


@customer_router.delete("/customers/{customer_id}")
def delete_customer(customer_id: str):
    try:
        logger.info(f"Deleting customer with id={customer_id}")
        customer_service.delete_customer(customer_id)

        logger.info("Delete customer request finished with response=204")
        return Response(status_code=204)

    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@customer_router.put("/customers/", response_model=Customer_update)
def update_customer(customer_update: Customer):
    logger.info(f"Starting the process to full update customer {customer_update}")
    try:
        logger.info("Full update customer request finished with response=200")
        return customer_service.update_customer(customer_update)

    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)


@customer_router.patch("/customers/", response_model=Customer_update)
def patch_customer(customer_update: Customer_update):
    logger.info(f"Starting the process to partial update customer {customer_update}")
    try:
        logger.info("Partial update customer request finished with response=200")
        return customer_service.patch_customer(customer_update)

    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
