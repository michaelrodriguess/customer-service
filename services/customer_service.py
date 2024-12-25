from storage.customers_storage import CustomerStorage
from models.customer import Customer, Customer_update


class Customer_service:

    def __init__(self):
        self.storage = CustomerStorage()

    def update_customer(self, id: str, customer: Customer):

        updated_customer = self.storage.update_customer(id, customer)

        return updated_customer

    def patch_customer(self, id: str, customer: Customer_update):

        updated_customer = self.storage.patch_customer(id, customer)

        return updated_customer
