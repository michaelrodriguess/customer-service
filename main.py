from fastapi import FastAPI
import logging
from routes.customer_router import router

logger = logging.getLogger(__name__)
app = FastAPI()

app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}
