from config.db_conn import conn
from psycopg2 import sql, Error
from datetime import datetime, timezone, timedelta


class CustomerStorage:
    def __init__(self):
        self.customers = []
        self.db = conn

    def update_customer(self, customer_update) -> dict:
        try:
            utc_minus_3 = timezone(timedelta(hours=-3))
            with self.db.cursor() as cursor:
                query = sql.SQL(
                    """
                                UPDATE customers
                                SET name =%s, email =%s, updated_at=%s
                                WHERE id = %s
                                RETURNING id, name, email, updated_at """
                )
                # TODO organizar o horário, tá batendo como utc:0, tmj
                cursor.execute(
                    query,
                    (
                        customer_update.name,
                        customer_update.email,
                        datetime.now(timezone.utc).astimezone(utc_minus_3),
                        customer_update.id,
                    ),
                )

                updated_customer = cursor.fetchone()

                if not updated_customer:
                    raise EntityNotFound(
                        f"Customer with id {customer_update.id} not found"
                    )

                self.db.commit()
                return updated_customer

        except (Error, ValueError):
            self.db.rollback()
            raise

    def patch_customer(self, customer_update) -> dict:
        try:
            with conn.cursor() as cursor:
                update_data = {
                    key: value
                    for key, value in customer_update.dict().items()
                    if value is not None and key != "id"
                }
                set_string = ",".join([f"{key} = %s" for key in update_data])

                query = sql.SQL(
                    "UPDATE customers SET {set_string} WHERE id =%s RETURNING id,name,email,updated_at"
                ).format(set_string=sql.SQL(set_string))
                cursor.execute(query, list(update_data.values()) + [customer_update.id])

                updated_customer = cursor.fetchone()

                if not updated_customer:
                    raise EntityNotFound(
                        f"Customer with id {customer_update.id} not found"
                    )

                self.db.commit()
                return updated_customer
        except (Error, ValueError):
            self.db.rollback()
            raise


class EntityNotFound(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
