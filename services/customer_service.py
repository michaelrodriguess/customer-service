import logging
from storages.customer_storage import CustomerStorage
from models.customer import Customer


class CustomerService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.storage = CustomerStorage()

        
    def create_customer(self, customer: Customer):
        self.logger.info(f"Creating customer with this data={customer}")
        return self.storage.create_customer(customer)

    def delete_customer(self, customer_id: str):
        self.logger.info(f"Deleting customer with id={customer_id}")
        self.storage.delete_customer(customer_id)

