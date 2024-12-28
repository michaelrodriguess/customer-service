import logging
from fastapi import APIRouter, HTTPException, Response
from services.customer_service import CustomerService
from psycopg2 import DatabaseError

logging.basicConfig(
    format="%(asctime)s - %(message)s",
    level=logging.INFO
)

customer_router = APIRouter()
logger = logging.getLogger(__name__)
customer_service = CustomerService()

@customer_router.delete("/customers/{customer_id}")
def delete_customer(customer_id: str):
    try:
        logger.info(f"Deleting customer with id={customer_id}")
        customer_service.delete_customer(customer_id)
    
        logger.info("Delete customer request finished with response=204")
        return Response(status_code=204)

    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
