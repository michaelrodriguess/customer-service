from fastapi import FastAPI
from routes.customer_router import customer_router

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

app.include_router(customer_router)