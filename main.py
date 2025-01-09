"""
This module handles the initialisation of FastApi
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from configs.db_conn import get_database_connection
from services.customer_service import CustomerService
from storages.customer_storage import CustomerStorage
from routes.customer_router import router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Method that handles FastApi configuration
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
    Healthy check to see if the application is working in a basic way
    """
    return {"status": "healthy"}

