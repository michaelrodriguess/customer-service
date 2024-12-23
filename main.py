from fastapi import FastAPI
from routes import customers

app = FastAPI()
app.include_router(customers)
