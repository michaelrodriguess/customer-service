import logging
from typing import List
from storages.customer_storage import CustomerStorage
from models.customer_model import Customer_update, Customer
import logging


class Customer_service:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.storage = CustomerStorage()

    def get_customer_by_id(self, id: str) -> Customer:
        self.logger.info(f"Getting customer by id...")
        return self.storage.get_customer_by_id(id)

    def get_all_customers(self) -> List[Customer]:
        self.logger.info(f"Getting all customers...")
        return self.storage.get_all_customers()

    def create_customer(self, customer: Customer):
        self.logger.info(f"Creating customer with this data={customer}")
        return self.storage.create_customer(customer)

    def update_customer(self, customer) -> Customer_update:
        self.logger.info("Starting the service to update customer")
        updated_customer = self.storage.update_customer(customer)
        return updated_customer

    def patch_customer(self, customer) -> Customer_update:
        self.logger.info("Starting the service to update customer")
        updated_customer = self.storage.patch_customer(customer)
        return updated_customer

    def delete_customer(self, customer_id: str):
        self.logger.info(f"Deleting customer with id={customer_id}")
        self.storage.delete_customer(customer_id)
