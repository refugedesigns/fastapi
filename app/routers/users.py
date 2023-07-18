from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import schemas, models
from ..utils.authorize_permissions import get_current_user, admin_routes

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/", response_model=List[schemas.UserResponse], dependencies=[Depends(admin_routes)])
def get_all_users(db: Session = Depends(get_db), limit: int = 10, skip: int = 0):
    users = db.query(models.User).limit(limit).offset(skip).all()
    return users


@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {user_id} not found")

    return user
