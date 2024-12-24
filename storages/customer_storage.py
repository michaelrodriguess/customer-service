import logging
from models.customer import Customer
from config.db_conn import db_conn

class CustomerStorage:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db = db_conn
        
    def create_customer(self, customer: Customer) -> Customer:
        self.logger.info(f"[STORAGE]: Creating customer with email={customer.email}")

        try:
            with self.db.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO customers (id, name, email, created_at, updated_at)
                    VALUES (%s, %s, %s, NOW(), NOW());
                    """,
                    (customer.id, customer.name, customer.email),
                )
                self.db.commit()
                return customer
            
        except Exception as ex:
            self.logger.error(f"Error in storage layer: {ex}")
            raise
