import logging
from typing import List
from psycopg2 import DatabaseError, IntegrityError, sql
from psycopg2._psycopg import connection
from datetime import datetime
from exceptions.customer_exceptions import EntityNotFound
from models.customer_model import Customer_update, Customer


class CustomerStorage:
    def __init__(self, db_connection: connection):
        self.logger = logging.getLogger(__name__)
        self.db = db_connection

    def get_customer_by_id(self, id: str) -> Customer:
        self.logger.info("Getting an customer in DB")
        try:
            with self.db.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, name, email, created_at, updated_at, active
                    FROM customers
                    WHERE id = %s AND active = true;
                    """,
                    (id,),
                )

                result = cursor.fetchone()

                if result == None:
                    raise ValueError(f"Customer not found with id {id}")

                return self.map_customer_row_to_model(result)

        except DatabaseError as ex:
            self.logger.error(f"Failed to get customer by id={id} in DB. Error: {ex}")
            raise

    def get_all_customers(self) -> List[Customer]:
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
            self.logger.error(f"Failed to get all customers in DB. Error: {ex}")
            raise

    def create_customer(self, customer: Customer) -> Customer:
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
                self.logger.info(f"Customer {customer.name} successfully inserted.")
                return customer

        except IntegrityError as integrity_error:
            self.db.rollback()
            self.logger.error(
                f"Integrity error while inserting customer. Customer data: {customer}."
                f"Details: {integrity_error}"
            )
            raise

        except DatabaseError as db_error:
            self.db.rollback()
            self.logger.error(
                f"Database error while inserting customer. Customer data: {customer}. "
                f"Details: {db_error}"
            )
            raise

    def delete_customer(self, customer_id: str):
        self.logger.info(f"Deleting customer with id {customer_id}")
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
            self.logger.error(f"Failed to delete in DB: {ex}")
            raise

    def map_customer_row_to_model(self, row: List) -> Customer:
        return Customer(
            id=row[0], name=row[1], email=row[2], created_at=row[3], updated_at=row[4]
        )

    def update_customer(self, customer_update) -> Customer_update:
        self.logger.info(
            f" Full updating customer: {customer_update.name}, with id: {customer_update.id}"
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
                self.logger.error(f"Customer {customer_update.name} updated in DB")
                return self.customerTransform(updated_customer)

        except IntegrityError as integrity_error:
            self.db.rollback()
            self.logger.error(
                f"Integrity error while updating customer. Customer data: {customer_update}."
                f"Details: {integrity_error}"
            )
            raise

        except DatabaseError as ex:
            self.db.rollback()
            self.logger.error("Failed to update in DB: {ex}")
            raise

    def patch_customer(self, customer_update) -> Customer_update:
        self.logger.info(
            f"Partial updating customer: {customer_update.name}, with id: {customer_update.id}"
        )
        try:
            with self.db.cursor() as cursor:
                update_data = {
                    key: value
                    for key, value in customer_update.dict().items()
                    if value is not None and key != "id"
                }
                set_string = ",".join([f"{key} = %s" for key in update_data])

                query = sql.SQL(
                    "UPDATE customers SET {set_string} WHERE id =%s RETURNING id, name, email, active, updated_at"
                ).format(set_string=sql.SQL(set_string))
                cursor.execute(query, list(update_data.values()) + [customer_update.id])

                updated_customer = cursor.fetchone()

                if not updated_customer:
                    raise EntityNotFound(
                        f"Customer with id {customer_update.id} not found"
                    )

                self.db.commit()
                self.logger.error(f"Customer {customer_update.name} updated in DB")
                return self.customerTransform(updated_customer)

        except IntegrityError as integrity_error:
            self.db.rollback()
            self.logger.error(
                f"Integrity error while updating customer. Customer data: {customer_update}."
                f"Details: {integrity_error}"
            )
            raise

        except DatabaseError as ex:
            self.db.rollback()
            self.logger.error(f"Failed to update in DB: {ex}")
            raise

    def customerTransform(self, customerTuple: tuple) -> Customer_update:
        return Customer_update(
            id=customerTuple[0],
            name=customerTuple[1],
            email=customerTuple[2],
            active=customerTuple[3],
            updated_at=customerTuple[4],
        )
