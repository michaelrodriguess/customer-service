from storage.customers_storage import CustomerStorage
from models.customer import Customer


class Customer_service:

    def __init__(self):
        self.storage = CustomerStorage()

    def update_customer(self, id: int, customer: Customer):

        updated_customer = self.storage.update_customer(id, customer)

        return updated_customer
