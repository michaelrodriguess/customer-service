import logging
from fastapi import APIRouter
from models.customer import Customer
from services.customer_service import CustomerService


logging.basicConfig(
    format="%(asctime)s - %(message)s",
    level=logging.INFO
)

router = APIRouter()
logger = logging.getLogger(__name__)
customer_service = CustomerService()

@router.post("/customers", response_model=Customer)
def create_customer(customer_data: Customer):
    logger.info(f"[ROUTER]: Creating customer with email={customer_data.email}")
    created_customer = customer_service.create_customer(customer_data)
    
    logger.info(f"create customer request finished with response={customer_data.model_dump()}")
    return created_customer
