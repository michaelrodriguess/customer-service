from fastapi import FastAPI
import logging
from routes.customer_router import customer_router

logger = logging.getLogger(__name__)
app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

app.include_router(customer_router)
