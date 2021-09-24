from fastapi import FastAPI
from fastapi import Depends
from fastapi.responses import JSONResponse
from db import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/hello_world")
def hello_world(db=Depends(get_db)):
    return JSONResponse(status_code=200, content={
        "hello": "world",
    })
