"""
Esse módulo lida com as regras de negócio, chamando a storage.
"""

import logging
from typing import List
from storages.customer_storage import CustomerStorage
from models.customer_model import CustomerUpdate, Customer


class CustomerService:
    """
    Classe que lida com o tratamento de regras de negócio relacionadas a clientes.
    """

    def __init__(self, storage: CustomerStorage):
        """
        Inicializa o serviço com a instância de armazenamento fornecida.

        Args:
            storage (CustomerStorage): Instância responsável por acessar os dados do cliente.
        """
        self.logger = logging.getLogger(__name__)
        self.storage = storage

    def get_customer_by_id(self, id_customer: str) -> Customer:
        """
        This method delegates the retrieval of a customer to the `storage` layer, 
        which fetches the customer record from the database based on the provided ID.
        """
        self.logger.info("Getting customer by id...")
        return self.storage.get_customer_by_id(id_customer)

    def get_all_customers(self) -> List[Customer]:
        """
        This method delegates the retrieval of all customer records to the `storage` layer, 
        which handles the database operations. It returns a list of `Customer` objects 
        representing all customers in the system.
        """
        self.logger.info("Getting all customers...")
        return self.storage.get_all_customers()

    def create_customer(self, customer: Customer) -> Customer:
        """
        Cria um novo cliente com os dados fornecidos.

        Args:
            customer (Customer): Dados do cliente a ser criado.

        Returns:
            Customer: Dados do cliente criado.
        """
        self.logger.info("Creating customer with this data=%s", customer)
        return self.storage.create_customer(customer)

    def update_customer(self, customer: Customer) -> CustomerUpdate:
        """
        Atualiza completamente os dados de um cliente.

        Args:
            customer (Customer): Dados atualizados do cliente.

        Returns:
            CustomerUpdate: Dados do cliente após a atualização.
        """
        self.logger.info("Starting the service to update customer")
        updated_customer = self.storage.update_customer(customer)
        return updated_customer

    def patch_customer(self, customer: CustomerUpdate) -> CustomerUpdate:
        """
        Atualiza parcialmente os dados de um cliente.

        Args:
            customer (CustomerUpdate): Dados parciais a serem atualizados.

        Returns:
            CustomerUpdate: Dados do cliente após a atualização parcial.
        """
        self.logger.info("Starting the service to update customer")
        updated_customer = self.storage.patch_customer(customer)
        return updated_customer

    def delete_customer(self, customer_id: str):
        """
        Remove um cliente do sistema pelo ID.

        Args:
            customer_id (str): Identificador único do cliente a ser removido.

        Returns:
            None
        """
        self.logger.info("Deleting customer with id=%s", customer_id)
        self.storage.delete_customer(customer_id)
