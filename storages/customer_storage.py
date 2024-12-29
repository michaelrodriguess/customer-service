import logging
from config.db_conn import db_conn
from psycopg2 import DatabaseError, sql, Error
from datetime import datetime
from exceptions.customer_exceptions import EntityNotFound
from models.customer_model import Customer_update


class CustomerStorage:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db = db_conn

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
                    for key, value in customer_update.dict(exclude_unset=True).items()
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
