import logging
from storages.customer_storage import CustomerStorage
from models.customer import Customer

class CustomerService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.storage = CustomerStorage()
        
    def create_customer(self, customer: Customer):
        self.logger.info(f"[SERVICE]: Creating customer with email={customer.email}")
        try:     
            return self.storage.create_customer(customer)
        except Exception as ex:
            self.logger.error(f"Error in service layer: {ex}")
            raise