from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Union
from ..database import get_db
from ..utils.authorize_permissions import get_current_user
from .. import schemas, models

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.get("/", response_model=List[schemas.PostOut])
def get_all_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                                                                                         models.Vote.post_id == models.Post.id,
                                                                                         isouter=True).group_by(
        models.Post.id)
    results = results.filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = list(map(lambda x: x._mapping, results))
    return results


@router.get("/{post_id}", response_model=schemas.PostOut)
def get_single_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                                                                                      models.Vote.post_id == models.Post.id,
                                                                                      isouter=True).group_by(
        models.Post.id).filter(
        models.Post.id == post_id).first()
    post = post._mapping if post else None
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {post_id} not found.")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    print(current_user)
    new_post = models.Post(user_id=current_user["id"], **post.dict())  # unpack post object with key=value
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
