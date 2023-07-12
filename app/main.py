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


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:

    try:
        conn = psycopg2.connect(host='localhost',
                                database='fastapicourse',
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


@app.get("/")
def root():
    return {"message": "This is your post"}


# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     return {"status": "success"}


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cur.execute("""SELECT * FROM posts""")
    # posts = cur.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):  # title str, content str
    # cur.execute(
    #     """
    #     INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *
    #     """,
    #     (post.title, post.content, post.published)
    # )
    #
    # new_post = cur.fetchone()
    # conn.commit()

    new_post = models.Post(**post.dict())  # dict unpacking
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cur.execute(
    #     """
    #     SELECT * FROM posts WHERE id = %s
    #     """, (str(id),))  # the extra comma solves the problem here
    # post = cur.fetchone()

    # if not post:
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {'message': f"post with id: {id} was not found"}

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cur.execute(
    #     """
    #     DELETE FROM posts WHERE id = %s RETURNING *
    #     """, (str(id)),
    # )
    # deleted_post = cur.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cur.execute(
    #     """
    #     UPDATE posts SET
    #     title = %s, content = %s, published = %s
    #     WHERE id = %s
    #     RETURNING *
    #     """,
    #     (post.title, post.content, post.published, str(id))
    # )
    # updated_post = cur.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password - user.password
    hashed_password = utils.hash_pwd(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())  # dict unpacking
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
