from pymongo import MongoClient
import os

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(
    mongo_uri,
    username=os.getenv("MONGO_INITDB_ROOT_USERNAME"),
    password=os.getenv("MONGO_INITDB_ROOT_PASSWORD"),
)

db = client["users_db"]
users_collection = db["users"]
