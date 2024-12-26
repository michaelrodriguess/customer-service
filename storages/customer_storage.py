import logging
from models.customer import Customer
from config.db_conn import db_conn

class CustomerStorage:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db = db_conn
        
    def create_customer(self, customer: Customer) -> Customer:
        self.logger.info("Inserting product in DB")

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
            self.logger.error(f"Failed to insert customer with this data:{customer}. Error: {ex}")
            raise
