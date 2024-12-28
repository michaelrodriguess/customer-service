from fastapi import FastAPI
from routes.customer_route import CustomerRouter

app = FastAPI()

app.include_router(CustomerRouter)
