from fastapi import FastAPI
import logging
from routes.customer_router import router as customer_router

logger = logging.getLogger(__name__)
app = FastAPI()

app.include_router(customer_router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}
<<<<<<< HEAD
=======

app.include_router(customer_router)
>>>>>>> 42a2624cb02e7ac407be58180d2bb29a03ffae2a
