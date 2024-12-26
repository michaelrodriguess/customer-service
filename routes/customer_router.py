import logging
from fastapi import APIRouter
from models.customer import Customer
from services.customer_service import CustomerService

router = APIRouter()
logger = logging.getLogger(__name__)
customer_service = CustomerService()

@router.post("/customers", response_model=Customer)
def create_customer(customer_data: Customer):
    logger.info(f"Creating customer with this data={customer_data}")
    created_customer = customer_service.create_customer(customer_data)
    
    logger.info(f"create customer request finished with response={create_customer}")
    return created_customer
