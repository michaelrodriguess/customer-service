from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from mongodb import users_collection
from bson import ObjectId

app = FastAPI()


class User(BaseModel):
    name: str
    email: str


@app.post("/users/")
async def create_user(request: Request):
    try:
        data = await request.json()
        user = User(**data)
        user_data = user.dict()
        result = users_collection.insert_one(user_data)

        return {"id": str(result.inserted_id)}
    except Exception as e:

        raise HTTPException(status_code=400, detail=str(e))


class UpdateUser(BaseModel):
    name: str = None
    email: str = None
    age: int = None


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return {
            "name": user["name"],
            "email": user["email"],
        }

    raise HTTPException(status_code=404, detail="User not found")
