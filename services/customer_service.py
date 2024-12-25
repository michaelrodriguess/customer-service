import logging
from storages.customer_storage import CustomerStorage

class CustomerService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.storage = CustomerStorage()

    def delete_customer(self, customer_id: str):
        self.logger.info(f"[SERVICE]: Deleting customer with id={customer_id}")

        try:
            deleted_customer_id = self.storage.delete_customer(customer_id)
            if deleted_customer_id is None:
                self.logger.warning(f"[SERVICE]: No active customer found with id={customer_id}")
                return None
            return {"message": f"Customer id={customer_id} successfully deactivated."}
        
        except Exception as ex:
            self.logger.error(f"Error in service layer: {ex}")
            raise