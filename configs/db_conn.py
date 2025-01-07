"""
Arquivo de conexão do banco de dados Postgresql
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_database_connection():
    """
    Estabelece e retorna uma conexão com o banco de dados PostgreSQL.

    Este método utiliza variáveis de ambiente para recuperar as credenciais de
    acesso ao banco de dados, incluindo o nome do banco, host, usuário, senha
    e porta.

    Returns:
        connection: A conexão com o banco de dados PostgreSQL.
    """
    db_connection = psycopg2.connect(
        database=os.getenv("DATABASE_NAME"),
        host=os.getenv("DATABASE_HOST"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        port=os.getenv("DATABASE_PORT"),
    )
    return db_connection
