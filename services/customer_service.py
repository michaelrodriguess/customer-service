from storages.customers_storage import CustomerStorage
from models.customer_model import Customer_update


class Customer_service:

    def __init__(self):
        self.storage = CustomerStorage()

    def update_customer(self, customer) -> Customer_update:

        updated_customer = self.storage.update_customer(customer)

        updated_customer_dict = {
            "id": updated_customer[0],
            "name": updated_customer[1],
            "email": updated_customer[2],
            "updated_at": updated_customer[3],
        }
        return Customer_update(**updated_customer_dict)

    def patch_customer(self, customer) -> Customer_update:

        updated_customer = self.storage.patch_customer(customer)

        updated_customer_dict = {
            "id": updated_customer[0],
            "name": updated_customer[1],
            "email": updated_customer[2],
            "updated_at": updated_customer[3],
        }

        return Customer_update(**updated_customer_dict)
