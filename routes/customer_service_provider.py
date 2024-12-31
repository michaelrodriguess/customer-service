from services.customer_service import Customer_service
from storages.customer_storage import CustomerStorage

def get_customer_service() -> Customer_service:
    storage = CustomerStorage()
    return Customer_service(storage)
