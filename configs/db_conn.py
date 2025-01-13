"""
Postgresql database connection file
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_database_connection():
    """
    Establishes and returns a connection to the PostgreSQL database.
    This method uses environment variables to retrieve the credentials for
    credentials, including the database name, host, user, password
    and port.
    Returns:
        connection: The connection to the PostgreSQL database.
    """
    db_connection = psycopg2.connect(
        database=os.getenv("DATABASE_NAME"),
        host=os.getenv("DATABASE_HOST"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        port=os.getenv("DATABASE_PORT"),
    )
    return db_connection
