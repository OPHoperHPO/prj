from fastapi import FastAPI
from fastapi.responses import JSONResponse
import db

app = FastAPI()

@app.get("/hello_world")
def hello_world():
    return JSONResponse(status_code=200, content={
        "hello": "world",
    })
