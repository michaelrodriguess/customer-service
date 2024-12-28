from storages.customers_storage import CustomerStorage


class Customer_service:

    def __init__(self):
        self.storage = CustomerStorage()

    def update_customer(self, customer):

        updated_customer = self.storage.update_customer(customer)

        return updated_customer

    def patch_customer(self, customer):

        updated_customer = self.storage.patch_customer(customer)

        return updated_customer
