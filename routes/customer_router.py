from fastapi import APIRouter, HTTPException
from models.customer import Customer
import logging
from services.customer_service import CustomerService
from typing import List

router = APIRouter()

logger = logging.getLogger(__name__)
service = Customer()

@router.get("/customers", response_model=List[Customer])
def get_all_customers():
    try:
        customers = CustomerService.get_all_customers()
        return customers
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error: {str(ex)}")

@router.get("/customers/{id}", response_model=Customer)
def get_customer_by_id(id: str):
    try:
        customer = CustomerService.get_customer_by_id(id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error: {str(ex)}")
