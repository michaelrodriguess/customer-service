"""
This module deals with the business rules by calling storage.
"""

import logging
from typing import List
from storages.customer_storage import CustomerStorage
from models.customer_model import CustomerUpdate, Customer


class CustomerService:
    """
    Class that handles customer-related business rules.
    """

    def __init__(self, storage: CustomerStorage):
        """
        Args:
            storage (CustomerStorage): Instance responsible for accessing customer data.
        """
        self.logger = logging.getLogger(__name__)
        self.storage = storage

    def get_customer_by_id(self, id_customer: str) -> Customer:
        """
        Fetch a customer of the `storage` layer.
        """
        self.logger.info("Getting customer by id...")
        return self.storage.get_customer_by_id(id_customer)

    def get_all_customers(self) -> List[Customer]:
        """
        Fetch all customer records of the `storage` layer.
        """
        self.logger.info("Getting all customers...")
        return self.storage.get_all_customers()

    def create_customer(self, customer: Customer):
        """
        Args:
            customer (Customer): Data of the customer to be created.

        Returns:
            Customer: Data of the customer created.
        """
        self.logger.info("Creating customer with this data=%s", customer)
        return self.storage.create_customer(customer)

    def update_customer(self, customer: Customer) -> CustomerUpdate:
        """
        Args:
            customer (Customer): Updated customer data.

        Returns:
            CustomerUpdate: Customer data after the update.
        """
        self.logger.info("Starting the service to update customer")
        updated_customer = self.storage.update_customer(customer)
        return updated_customer

    def patch_customer(self, customer) -> CustomerUpdate:
        """
        Args:
            customer (CustomerUpdate): Partial data to be updated.

        Returns:
            CustomerUpdate: Customer data after the partial update.
        """
        self.logger.info("Starting the service to update customer")
        updated_customer = self.storage.patch_customer(customer)
        return updated_customer

    def delete_customer(self, customer_id: str):
        """
        Args:
            customer_id (str): Unique identifier of the customer to be removed.

        Returns:
            None
        """
        self.logger.info("Deleting customer with id=%s", customer_id)
        self.storage.delete_customer(customer_id)
