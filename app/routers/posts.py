from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import schemas, models

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.get("/", response_model=List[schemas.PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_single_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {post_id} not found.")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())  # unpack post object with key=value
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # retrieve new saved post from database
    return new_post


@router.put("/{post_id}")
def update_post(updated_post: schemas.CreatePost, post_id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {post_id} not found")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id)

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {post_id} not found")
    post.delete(synchronize_session=False)
    db.commit()
    return {"data": f"post with id: {post_id} deleted."}
