import logging
from fastapi import APIRouter, HTTPException
from services.customer_service import CustomerService

logging.basicConfig(
    format="%(asctime)s - %(message)s",
    level=logging.INFO
)

customer_router = APIRouter()
logger = logging.getLogger(__name__)
customer_service = CustomerService()


@customer_router.delete("/customers/{customer_id}")
def soft_delete_customer(customer_id: str):
    logger.info(f"[ROUTER]: Soft deleting customer with id={customer_id}")
    result = customer_service.delete_customer(customer_id)
    
    if result is None:
        raise HTTPException(status_code=404, detail="Customer not found or already inactive.")
    
    logger.info(f"delete customer request finished with response={result}")
    return result
