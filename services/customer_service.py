import logging
from models.customer import Customer
from storages.customer_storage import CustomerStorage
from typing import List
from models.customer import Customer


class CustomerService:

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

    def delete_customer(self, customer_id: str):
        self.logger.info(f"Deleting customer with id={customer_id}")
        self.storage.delete_customer(customer_id)