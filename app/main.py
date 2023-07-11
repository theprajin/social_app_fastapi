from typing import Optional
from random import randrange
import time

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


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

    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
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


@app.get("/posts")
def get_posts():
    cur.execute("""SELECT * FROM posts""")
    posts = cur.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):  # title str, content str
    cur.execute(
        """
        INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *
        """,
        (post.title, post.content, post.published)
    )

    new_post = cur.fetchone()
    conn.commit()
    print(new_post)

    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cur.execute(
        """
        SELECT * FROM posts WHERE id = %s
        """, (str(id),))  # the extra comma solves the problem here
    post = cur.fetchone()

    # if not post:
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {'message': f"post with id: {id} was not found"}
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cur.execute(
        """
        DELETE FROM posts WHERE id = %s RETURNING *
        """, (str(id)),
    )
    deleted_post = cur.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict

    return {"data": post_dict}
