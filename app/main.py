from fastapi import FastAPI

app = FastAPI()


@app.post("/api/v1/login")
async def login():
    return {"message": "Hello World"}
