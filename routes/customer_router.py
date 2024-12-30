from fastapi import APIRouter, HTTPException, Response
import logging
from typing import List
from services.customer_service import Customer_service
from models.customer_model import Customer, Customer_update
from exceptions.customer_exceptions import EntityNotFound

router = APIRouter()
logger = logging.getLogger(__name__)
customer_service = Customer_service()


@router.get("/customers", response_model=List[Customer])
def get_all_customers():
    logger.info(f"Getting all customers")
    get_customer = customer_service.get_all_customers()

    logger.info(
        f"Get all data of customers request finished with response={get_customer}"
    )
    return get_customer


@router.get("/customers/{id}", response_model=Customer)
def get_customer_by_id(id: str):
    try:
        logger.info(f"Gettin customer with id={id}")
        get_customer = customer_service.get_customer_by_id(id)

        logger.info(f"Get customer by id request finished with response={get_customer}")
        return get_customer
    except ValueError as ex:
        logger.warning(f"Customer not found: {ex}")
        raise HTTPException(status_code=404, detail=ex.message)


@router.post("/customers", response_model=Customer)
def create_customer(customer_data: Customer):
    logger.info(f"Creating customer with this data={customer_data}")
    created_customer = customer_service.create_customer(customer_data)

    logger.info(f"create customer request finished with response={create_customer}")
    return created_customer


@router.delete("/customers/{customer_id}")
def delete_customer(customer_id: str):
    try:
        logger.info(f"Deleting customer with id={customer_id}")
        customer_service.delete_customer(customer_id)

        logger.info("Delete customer request finished with response=204")
        return Response(status_code=204)

    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/customers/", response_model=Customer_update)
def update_customer(customer_update: Customer):
    logger.info(f"Starting the process to full update customer {customer_update}")
    try:

        updated_customer = customer_service.update_customer(customer_update)
        logger.info(
            f"Full update customer request finished with response={updated_customer}"
        )
        return updated_customer
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.patch("/customers/", response_model=Customer_update)
def patch_customer(customer_update: Customer_update):
    logger.info(f"Starting the process to partial update customer {customer_update}")
    try:
        updated_customer = customer_service.patch_customer(customer_update)
        logger.info(
            f"Full update customer request finished with response={updated_customer}"
        )
        return updated_customer
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
