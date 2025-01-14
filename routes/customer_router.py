"""
This module handles customer routes.
"""

import logging
from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Response, Depends, Request, status

from services.customer_service import CustomerService
from models.customer_model import Customer, CustomerUpdate
from exceptions.customer_exceptions import EntityNotFound

router = APIRouter()
logger = logging.getLogger(__name__)


def get_customer_service(request: Request):
    """

    Args:
        request (Request): Object of the current request.

    Returns:
        CustomerService: Customer service.
    """
    return request.state.customer_service


ServiceDep = Annotated[CustomerService, Depends(get_customer_service)]


@router.get("/customers", response_model=List[Customer])
def get_all_customers(service: ServiceDep):
    """
    This endpoint handles HTTP GET requests to fetch a list of all customers.
    """
    logger.info("Getting all customers")
    customers = service.get_all_customers()

    logger.info(
        "Get all data of customers request finished with response=%s", customers
    )
    return customers


@router.get("/customers/{customer_id}", response_model=Customer)
def get_customer_by_id(customer_id: str, service: ServiceDep):
    """
    This endpoint handles HTTP GET requests to fetch a customer by ID.
    """
    try:
        logger.info("Getting customer with id=%s", customer_id)
        customer = service.get_customer_by_id(customer_id)
        logger.info("Get customer by id request finished with response=%s", customer)
        return customer
    except ValueError as ex:
        logger.warning("Customer not found: id=%s", id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found with id {id}",
        ) from ex


@router.post("/customers", status_code=status.HTTP_201_CREATED, response_model=Customer)
def create_customer(customer_data: Customer, service: ServiceDep):
    """
    Creates a new client.
    """
    logger.info("Creating customer with this data=%s", customer_data)
    created_customer = service.create_customer(customer_data)
    logger.info("Create customer request finished with response=%s", created_customer)
    return created_customer


@router.delete("/customers/{customer_id}")
def delete_customer(customer_id: str, service: ServiceDep):
    """
    Args:
        customer_id (str): Customer ID.
        service (CustomerService): Customer service.

    Returns:
        Response: HTTP response with status 204.

    Raises:
        HTTPException: If the customer is not found.
    """
    try:
        logger.info("Deleting customer with id=%s", customer_id)
        service.delete_customer(customer_id)
        logger.info("Delete customer request finished with response=204")
        return Response(status_code=204)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.put("/customers", response_model=CustomerUpdate)
def update_customer(customer_update: Customer, service: ServiceDep):
    """
    Args:
        customer_update (Customer): Customer data to be updated.
        service (CustomerService): Customer service.

    Returns:
        CustomerUpdate: Customer updated.

    Raises:
        HTTPException: If the customer is not found.
    """
    logger.info("Starting the process to fully update customer %s", customer_update)
    try:
        updated_customer = service.update_customer(customer_update)
        logger.info(
            "Full update customer request finished with response=%s", updated_customer
        )
        return updated_customer
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=e.message) from e


@router.patch("/customers", response_model=CustomerUpdate)
def patch_customer(customer_update: CustomerUpdate, service: ServiceDep):
    """
    Args:
        customer_update (CustomerUpdate): Customer data to be updated.
        service (CustomerService): Customer service.

    Returns:
        CustomerUpdate: Customer updated.

    Raises:
        HTTPException: If the customer is not found.
    """
    logger.info("Starting the process to partially update customer %s", customer_update)
    try:
        updated_customer = service.patch_customer(customer_update)
        logger.info(
            "Partial update customer request finished with response=%s",
            updated_customer,
        )
        return updated_customer
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=e.message) from e
