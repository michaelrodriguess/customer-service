"""
Module for storing customer-related data.
This module contains the `CustomerStorage` class, which manages CRUD operations
operations on the PostgreSQL database for customer data. It includes methods for
get, create, update, delete and list customers, as well as assisting in mapping
mapping between the database and customer models.
Functions:
    - get_customer_by_id: Searches for a customer by ID.
    - get_all_customers: Gets all active customers.
    - create_customer: Creates a new customer.
    - delete_customer: Marks a customer as inactive.
    - update_customer: Updates a customer's data.
    - patch_customer: Partially updates a customer's data.
    - customer_transform: Converts a customer's data into a tuple for the `CustomerUpdate` model.
"""

import logging
from datetime import datetime
from typing import List
from psycopg2 import DatabaseError, IntegrityError, sql
from psycopg2._psycopg import connection
from exceptions.customer_exceptions import EntityNotFound
from models.customer_model import CustomerUpdate, Customer


class CustomerStorage:
    """
    This class handles customer data in the PostgreSQL database.
    """
    def __init__(self, db_connection: connection):
        """
        Initialises the class with the database connection.

        Args:
            db_connection (connection): Connection to the PostgreSQL database.
        """
        self.logger = logging.getLogger(__name__)
        self.db = db_connection

    def get_customer_by_id(self, id_customer: str) -> Customer:
        """
        This method fetches a customer record from the `customers` table based on the provided 
        customer ID. Only active customers (`active = true`) are considered. If no matching record 
        is found, a ValueError is raised.
        """
        self.logger.info("Getting a customer by ID in DB")
        try:
            with self.db.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, name, email, created_at, updated_at, active
                    FROM customers
                    WHERE id = %s AND active = true;
                    """,
                    (id_customer,),
                )

                result = cursor.fetchone()

                if result is None:
                    raise ValueError(f"Customer not found with id {id_customer}")

                return self.map_customer_row_to_model(result)

        except DatabaseError as ex:
            self.logger.error(
                "Failed to get customer by id=%s in DB. Error:%s", id_customer, ex
            )
            raise

    def get_all_customers(self) -> List[Customer]:
        """
        This method queries the `customers` table to fetch all customer records where the 
        `active` status is set to `true`. The retrieved rows are mapped into `Customer` objects.
        """
        self.logger.info("Getting all customers in DB")
        try:
            with self.db.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, name, email, created_at, updated_at, active
                    FROM customers
                    WHERE active = true;
                    """
                )
                rows = cursor.fetchall()

                return [self.map_customer_row_to_model(row) for row in rows]
        except DatabaseError as ex:
            self.logger.error("Failed to get all customers in DB. Error: %s", ex)
            raise

    def create_customer(self, customer: Customer) -> Customer:
        """
        Creates a new client in the database.

        Args:
            customer (Customer): Instance of the customer to be created.

        Returns:
            Customer: The customer created.

        Raises:
            IntegrityError: If there is an integrity error in the database.
            DatabaseError: If there is an error inserting the customer into the database.
        """
        self.logger.info("Starting operation to insert customer into the database.")
        try:
            with self.db.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO customers (id, name, email, created_at, active)
                    VALUES (%s, %s, %s, NOW(), TRUE);
                    """,
                    (customer.id, customer.name, customer.email),
                )
                self.db.commit()
                self.logger.info("Customer %s successfully inserted.", customer.name)
                return customer

        except IntegrityError as integrity_error:
            self.db.rollback()
            self.logger.error(
                "Integrity error while inserting customer. Customer data: %s. Details: %s",
                customer,
                integrity_error,
            )
            raise

        except DatabaseError as db_error:
            self.db.rollback()
            self.logger.error(
                "Database error while inserting customer. Customer data: %s. Details: %s",
                customer,
                db_error,
            )
            raise

    def delete_customer(self, customer_id: str):
        """
        Marks a customer as inactive in the database.

        Args:
            customer_id (str): The ID of the customer to be deleted.

        Raises:
            DatabaseError: If an error occurs when accessing the database.
            KeyError: If the customer is not found or is already inactive.
        """
        self.logger.info("Deleting customer with id %s", customer_id)
        try:
            with self.db.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE customers
                    SET active = FALSE, updated_at = NOW()
                    WHERE id = %s AND active = TRUE;
                    """,
                    (customer_id,),
                )
                self.db.commit()
                if cursor.rowcount == 0:
                    raise KeyError(
                        f"Customer id={customer_id} not found or already inactive."
                    )

        except DatabaseError as ex:
            self.db.rollback()
            self.logger.error("Failed to delete customer in DB: %s", ex)
            raise

    def map_customer_row_to_model(self, row: List) -> Customer:
        """
        Maps a database row to a client model.

        Args:
            row (List): The row retrieved from the database.

        Returns:
            Customer: The mapped customer model.
        """
        return Customer(
            id=row[0], name=row[1], email=row[2], created_at=row[3], updated_at=row[4]
        )

    def update_customer(self, customer_update) -> CustomerUpdate:
        """
        Updates a client in the database with the new data provided.

        Args:
            customer_update (CustomerUpdate): The updated customer data.

        Returns:
            CustomerUpdate: The updated customer.

        Raises:
            EntityNotFound: If the customer is not found.
            IntegrityError: If there is an integrity error in the database.
            DatabaseError: If an error occurs when updating the customer's data.
        """
        self.logger.info(
            "Updating customer: %s, with id: %s",
            customer_update.name,
            customer_update.id,
        )
        try:
            with self.db.cursor() as cursor:
                query = sql.SQL(
                    """
                                UPDATE customers
                                SET name =%s, email =%s, updated_at=%s
                                WHERE id = %s and active = true
                                RETURNING id, name, email, active, updated_at """
                )
                cursor.execute(
                    query,
                    (
                        customer_update.name,
                        customer_update.email,
                        datetime.now(),
                        customer_update.id,
                    ),
                )

                updated_customer = cursor.fetchone()

                if not updated_customer:
                    raise EntityNotFound(
                        f"Customer with id {customer_update.id} not found"
                    )

                self.db.commit()
                self.logger.info("Customer %s updated in DB", customer_update.name)
                return self.customer_transform(updated_customer)

        except IntegrityError as integrity_error:
            self.db.rollback()
            self.logger.error(
                "Integrity error while updating customer. Customer data: %s. Details: %s",
                customer_update,
                integrity_error,
            )
            raise

        except DatabaseError as ex:
            self.db.rollback()
            self.logger.error("Failed to update customer in DB: %s", ex)
            raise

    def patch_customer(self, customer_update: CustomerUpdate) -> CustomerUpdate:
        """
        Partially updates a customer's data in the database.

        Args:
            customer_update (CustomerUpdate): The updated customer data.

        Returns:
            CustomerUpdate: The updated customer.

        Raises:
            EntityNotFound: If the customer is not found.
            IntegrityError: If there is an integrity error in the database.
            DatabaseError: If an error occurs when updating the customer's data.

        """
        self.logger.info(
            "Partial updating customer: %s, with id: %s",
            customer_update.name,
            customer_update.id,
        )
        try:
            with self.db.cursor() as cursor:
                update_data = {
                    key: value
                    for key, value in customer_update.dict().items()
                    if value is not None and key != "id"
                }
                set_string = sql.SQL(", ").join(
                    [sql.Identifier(key) + sql.SQL(" = %s") for key in update_data]
                )

                query = sql.SQL(
                    "UPDATE customers SET {set_string} WHERE id = %s RETURNING id, name, email, active, updated_at"
                ).format(set_string=set_string)
                cursor.execute(query, list(update_data.values()) + [customer_update.id])

                updated_customer = cursor.fetchone()

                if not updated_customer:
                    raise EntityNotFound(
                        f"Customer with id {customer_update.id} not found"
                    )

                self.db.commit()
                self.logger.info("Customer %s updated in DB", customer_update.name)
                return self.customer_transform(updated_customer)

        except IntegrityError as integrity_error:
            self.db.rollback()
            self.logger.error(
               "Integrity error while updating customer. Customer data: %s. Details: %s",
                customer_update,
                integrity_error,
            )
            raise

        except DatabaseError as ex:
            self.db.rollback()
            self.logger.error("Failed to update customer in DB: %s", ex)
            raise


    def customer_transform(self, customer_tuple: tuple) -> CustomerUpdate:
        """
        Converts a customer's data into a tuple for the CustomerUpdate model.

        Args:
            customer_tuple (tuple): The tuple containing the customer's data.

        Returns:
            CustomerUpdate: The transformed customer model.
        """
        return CustomerUpdate(
            id=customer_tuple[0],
            name=customer_tuple[1],
            email=customer_tuple[2],
            active=customer_tuple[3],
            updated_at=customer_tuple[4],
        )
