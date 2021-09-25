from fastapi import FastAPI
from fastapi import Depends
from fastapi.responses import JSONResponse
from db import SessionLocal, engine
from models import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


import auth
