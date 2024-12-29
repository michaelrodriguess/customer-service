import logging
from fastapi import APIRouter, HTTPException, Response
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

@router.delete("/customers/{customer_id}")
def delete_customer(customer_id: str):
    try:
        logger.info(f"Deleting customer with id={customer_id}")
        customer_service.delete_customer(customer_id)
    
        logger.info("Delete customer request finished with response=204")
        return Response(status_code=204)

    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

