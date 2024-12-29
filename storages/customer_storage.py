import logging
import psycopg2
from psycopg2 import DatabaseError, IntegrityError
from models.customer import Customer
from config.db_conn import db_conn


class CustomerStorage:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db = db_conn
        
    def create_customer(self, customer: Customer) -> Customer:
        self.logger.info("Starting operation to insert customer into the database.")

        try:            
            with self.db.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO customers (id, name, email, created_at)
                    VALUES (%s, %s, %s, NOW());
                    """,
                    (customer.id, customer.name, customer.email),
                )
                self.db.commit()
                self.logger.info(f"Customer {customer.name} successfully inserted.")
                return customer
                  
        except IntegrityError as integrity_error:
            self.db.rollback()
            self.logger.error(
                f"Integrity error while inserting customer. Customer data: {customer}. Details: {integrity_error}"
            )
            raise
        
        except DatabaseError as db_error:
            self.db.rollback()
            self.logger.error(
                f"Database error while inserting customer. Customer data: {customer}. "
                f"Details: {db_error}"
            )
            raise