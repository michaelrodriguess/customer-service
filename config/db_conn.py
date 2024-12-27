import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

load_dotenv()

db_conn = psycopg2.connect(
    database=os.getenv("DATABASE_NAME"),
    host=os.getenv("DATABASE_HOST"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    port=os.getenv("DATABASE_PORT"),
)

db_conn.cursor_factory = psycopg2.extras.DictCursor