from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, utils, oauth2

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.Post])
def get_posts(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    # cur.execute("""SELECT * FROM posts""")
    # posts = cur.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):  # title str, content str
    # cur.execute(
    #     """
    #     INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *
    #     """,
    #     (post.title, post.content, post.published)
    # )
    #
    # new_post = cur.fetchone()
    # conn.commit()
    print(current_user)
    new_post = models.Post(**post.dict())  # dict unpacking
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
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


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
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


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
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
