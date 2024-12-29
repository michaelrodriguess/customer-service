import logging
from models.customer import Customer
from config.db_conn import db_conn
from typing import List
from psycopg2 import DatabaseError, IntegrityError

class CustomerStorage:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db = db_conn
    
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
                    (id,))
                
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
                    """)
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
        self.logger.info(f"Deleting customer whit id {customer_id}")
        try:
            with self.db.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE customers
                    SET active = FALSE, updated_at = NOW()
                    WHERE id = %s AND active = TRUE;
                    """,
                    (customer_id,)
                )
                self.db.commit()
                if cursor.rowcount == 0:
                    raise KeyError(f"Customer id={customer_id} not found or already inactive.")
            
        except DatabaseError as ex:
            self.db.rollback()
            self.logger.error(f"Failed to delete in DB: {ex}")
            raise
            
    def map_customer_row_to_model(self, row: List) -> Customer:
        return customer(
            id = row[0],
            name = row[1],
            email = row[2],
            created_at = row[3],
            updated_at = row[4]
        )