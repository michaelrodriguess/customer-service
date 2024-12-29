from fastapi import APIRouter, HTTPException
from models.customer import Customer
import logging
from services.customer_service import CustomerService
from typing import List
from psycopg2 import DatabaseError


router = APIRouter()
logger = logging.getLogger(__name__)
customer_service = CustomerService()

@router.get("/customers", response_model=List[Customer])
def get_all_customers():
    try:
        return customer_service.get_all_customers()
    except DatabaseError as ex:
        logger.warning(f"Failed to get Customer: {ex}")
        raise HTTPException(status_code=500, detail=str(ex))

@router.get("/customers/{id}", response_model=Customer)
def get_customer_by_id(id: str):
    try:
        return customer_service.get_customer_by_id(id)
    except ValueError as ex:
        logger.warning(f"Customer not found: {ex}")
        raise HTTPException(status_code=404, detail=str(ex))
    except DatabaseError as ex:
        logger.warning(f"Failed to get Customer: {ex}")
        raise HTTPException(status_code=500, detail=str(ex))