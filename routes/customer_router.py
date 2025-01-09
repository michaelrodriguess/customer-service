from fastapi import APIRouter, HTTPException, Response, Depends, Request, status
import logging
from typing import Annotated, List
from configs.db_conn import get_database_connection
from services.customer_service import CustomerService
from storages.customer_storage import CustomerStorage
from models.customer_model import Customer, Customer_update
from exceptions.customer_exceptions import EntityNotFound

router = APIRouter()
logger = logging.getLogger(__name__)

def get_customer_service(request: Request):
    return request.state.customer_service

ServiceDep = Annotated[CustomerService, Depends(get_customer_service)]

@router.get("/customers", response_model=List[Customer])
def get_all_customers(service: ServiceDep):
    logger.info(f"Getting all customers")
    get_customer = service.get_all_customers()

    logger.info(
        f"Get all data of customers request finished with response={get_customer}"
    )
    return get_customer


@router.get("/customers/{id}", response_model=Customer)
def get_customer_by_id(id: str, service: ServiceDep):
    try:
        logger.info(f"Gettin customer with id={id}")
        get_customer = service.get_customer_by_id(id)

        logger.info(f"Get customer by id request finished with response={get_customer}")
        return get_customer
    except ValueError as ex:
        logger.warning(f"Customer not found: {ex}")
        raise HTTPException(status_code=404, detail=ex.message)


@router.post("/customers", status_code=status.HTTP_201_CREATED, response_model=Customer)
def create_customer(customer_data: Customer, service: ServiceDep):
    logger.info(f"Creating customer with this data={customer_data}")
    created_customer = service.create_customer(customer_data)

    logger.info(f"create customer request finished with response={create_customer}")
    return created_customer


@router.delete("/customers/{customer_id}")
def delete_customer(customer_id: str, service: ServiceDep):
    try:
        logger.info(f"Deleting customer with id={customer_id}")
        service.delete_customer(customer_id)

        logger.info("Delete customer request finished with response=204")
        return Response(status_code=204)

    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/customers", response_model=Customer_update)
def update_customer(customer_update: Customer, service: ServiceDep):
    logger.info(f"Starting the process to full update customer {customer_update}")
    try:

        updated_customer = service.update_customer(customer_update)
        logger.info(
            f"Full update customer request finished with response={updated_customer}"
        )
        return service
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.patch("/customers", response_model=Customer_update)
def patch_customer(customer_update: Customer_update, service: ServiceDep):
    logger.info(f"Starting the process to partial update customer {customer_update}")
    try:
        updated_customer = service.patch_customer(customer_update)
        logger.info(
            f"Full update customer request finished with response={updated_customer}"
        )
        return updated_customer
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
