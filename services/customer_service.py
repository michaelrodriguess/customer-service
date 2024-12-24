import logging
from models.customer import Customer
from storages.customer_storage import CustomerStorage
from typing import List

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