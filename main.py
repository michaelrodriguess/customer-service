import asyncpg
from contextlib import asynccontextmanager
from settings import settings
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    name: str
    email: str


@asynccontextmanager
async def get_db():
    conn = await asyncpg.connect(settings.DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()


async def create_user(conn, name: str, email: str):
    query = """
    INSERT INTO users (name, email)
    VALUES ($1, $2)
    RETURNING id
    """
    try:
        async with conn.transaction():
            user_id = await conn.fetchval(query, name, email)
        return user_id
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/users/")
async def create_user_endpoint(user: User):
    try:
        async with get_db() as db:
            user_id = await create_user(db, user.name, user.email)
        return {"id": user_id, "name": user.name, "email": user.email}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
