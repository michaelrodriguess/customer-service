"""
esse módulo lida com a inicialização do FastApi
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from configs.db_conn import get_database_connection
from services.customer_service import CustomerService
from storages.customer_storage import CustomerStorage
from routes.customer_router import router


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Método que lida com a configuração do FastApi
    """
    db_connection = get_database_connection()
    customer_storage = CustomerStorage(db_connection=db_connection)
    customer_service = CustomerService(customer_storage)

    yield {"customer_service": customer_service}
    logger.info("Shutdown application")


app = FastAPI(
    lifespan=lifespan,
    title="Customer Service",
)


app.include_router(router)


@app.get("/health")
def health_check():
    """
    Healthy check para saber se o aplicativo está funcionando de maneira básica
    """
    return {"status": "healthy"}
