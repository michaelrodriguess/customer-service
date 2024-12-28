from fastapi import APIRouter, HTTPException
from models.customer_model import Customer, Customer_update
from services.customer_service import Customer_service
from storages.customers_storage import EntityNotFound

customer_service = Customer_service()
CustomerRouter = APIRouter()


@CustomerRouter.put("/customers/")
def update_customer(customer_update: Customer):
    try:
        updated_customer = customer_service.update_customer(customer_update)

        return {
            "message": "Customer updated successfully",
            "customer": updated_customer,
        }

    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    except Exception:
        raise HTTPException(status_code=500, detail="an unexpected error ocurred.")


@CustomerRouter.patch("/customers/")
def patch_customer(customer_update: Customer_update):
    try:
        updated_customer = customer_service.patch_customer(customer_update)
        return {
            "customer": {
                "id": updated_customer[0],
                "name": updated_customer[1],
                "email": updated_customer[2],
                "updated_at": updated_customer[3],
            },
        }
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)

    except Exception:
        raise HTTPException(status_code=500, detail="an unexpected error ocurred.")
