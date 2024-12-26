from fastapi import FastAPI
from routes.customer_router import router as customer_router
import logging


logger = logging.getLogger(__name__)
app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

app.include_router(customer_router)
