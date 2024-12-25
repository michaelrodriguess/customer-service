import logging
from config.db_conn import db_conn

class CustomerStorage:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db = db_conn

    def delete_customer(self, customer_id: str):
        self.logger.info(f"[STORAGE]: Deleting customer whit id {customer_id}")

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
                    self.logger.warning(f"[STORAGE]: Customer id={customer_id} not found or already inactive.")
                    return None
                return customer_id
            
        except Exception as ex:
            self.logger.error(f"Error in storage layer: {ex}")
            raise