from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from routes.customer_router import get_customer_service
from configs.db_conn import get_database_connection
from services.customer_service import Customer_service
from storages.customer_storage import CustomerStorage
import logging
from routes.customer_router import router

logger = logging.getLogger(__name__)
@asynccontextmanager
async def lifespan(app: FastAPI):
    db_connection = get_database_connection()
    customer_storage = CustomerStorage(db_connection=db_connection)
    customer_service = Customer_service(customer_storage)
    
    yield {"customer_service": customer_service}
    logger.info(f"Shutdown application")
    
app = FastAPI(lifespan=lifespan, title="Customer Service",)

app.include_router(
    router,
    dependencies=[Depends(get_customer_service)]
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}
