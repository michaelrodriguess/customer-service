from storages.customer_storage import CustomerStorage
from models.customer_model import Customer_update
import logging


class Customer_service:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.storage = CustomerStorage()

    def update_customer(self, customer) -> Customer_update:
        self.logger.info(f"Starting the service to update customer")
        updated_customer = self.storage.update_customer(customer)
        return updated_customer

    def patch_customer(self, customer) -> Customer_update:
        self.logger.info(f"Starting the service to update customer")
        updated_customer = self.storage.patch_customer(customer)
        return updated_customer

    def delete_customer(self, customer_id: str):
        self.logger.info(f"Deleting customer with id={customer_id}")
        self.storage.delete_customer(customer_id)
