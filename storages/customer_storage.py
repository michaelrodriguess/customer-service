import logging
from models.customer import Customer
from config.db_conn import db_conn
from typing import List
from psycopg2 import DatabaseError

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

                return Customer(**result)

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

                return [Customer(**row) for row in rows]
        except DatabaseError as ex:
            self.logger.error(f"Failed to get all customers in DB. Error: {ex}")
            raise