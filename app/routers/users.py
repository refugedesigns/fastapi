from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import schemas, models
from ..utils.cookie_auth import get_current_user, authorize_permissions
from ..utils.hash import hash_password

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/", response_model=List[schemas.UserResponse], dependencies=[Depends(authorize_permissions)])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {user_id} not found")

    return user
