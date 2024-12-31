from fastapi import FastAPI, Depends
from routes.customer_router import get_customer_service
import logging
from routes.customer_router import customer_router

logger = logging.getLogger(__name__)
app = FastAPI()

app.include_router(
    customer_router,
    dependencies=[Depends(get_customer_service)]
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}
