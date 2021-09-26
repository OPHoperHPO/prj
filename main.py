from fastapi import FastAPI
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from db import SessionLocal, engine
from models import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://127.0.0.1:8080",
    "http://localhost:8080",
    "https://course-project-front.herokuapp.com",
    "https://news.asap-it.tech",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Access-Control-Expose-Headers
    expose_headers=["set-cookie"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


import auth
