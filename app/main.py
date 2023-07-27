from typing import Optional, List
from random import randrange
import time
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body, Depends
import psycopg2
from psycopg2.extras import RealDictCursor

from . import models, schemas, utils

from sqlalchemy.orm import Session
from .database import engine, get_db
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='postgres',
                                user='postgres',
                                password='root',
                                cursor_factory=RealDictCursor)
        cur = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as errors:
        print("Connecting to database failed")
        print("Error: ", errors)
        time.sleep(3)

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite food", "content": "I like pizza", "id": 2},
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "This is your post"}









