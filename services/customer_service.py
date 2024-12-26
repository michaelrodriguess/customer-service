import logging
from storages.customer_storage import CustomerStorage

class CustomerService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.storage = CustomerStorage()

    def delete_customer(self, customer_id: str):
        self.logger.info(f"Deleting customer with id={customer_id}")

        try:
            self.storage.delete_customer(customer_id)

        except Exception as ex:
            self.logger.error(f"Error in service layer: {ex}")
            raise