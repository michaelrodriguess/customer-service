from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def index(request: Request):
    return {"message": "Faith in god and children."}
