from fastapi import FastAPI
from routes.customers import CustomerRouter

app = FastAPI()

app.include_router(CustomerRouter)
