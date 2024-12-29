from fastapi import APIRouter, HTTPException
from models.customer import Customer
import logging
from services.customer_service import CustomerService
from typing import List
from psycopg2 import DatabaseError

logging.basicConfig(
    format="%(asctime)s - %(message)s",
    level=logging.INFO
)

router = APIRouter()
logger = logging.getLogger(__name__)
customer_service = CustomerService()

@router.get("/customers", response_model=List[Customer])
def get_all_customers():
    return customer_service.get_all_customers()

@router.get("/customers/{id}", response_model=Customer)
def get_customer_by_id(id: str):
    try:
        return customer_service.get_customer_by_id(id)
    except ValueError as ex:
        logger.warning(f"Customer not found: {ex}")
        raise HTTPException(status_code=404, detail=ex.message)

@customer_router.delete("/customers/{customer_id}")
def delete_customer(customer_id: str):
    try:
        logger.info(f"Deleting customer with id={customer_id}")
        customer_service.delete_customer(customer_id)
    
        logger.info("Delete customer request finished with response=204")
        return Response(status_code=204)

    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))