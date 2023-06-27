from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import List
from ..database import get_db
from .. import schemas, models

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")


@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"user with email {user.email} already exists.")

    hashed_pwd = pwd_context.hash(user.password)
    user.password = hashed_pwd

    new_user = models.User(**user.dict())  # unpack post object with key=value
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # retrieve new saved post from database
    return new_user


@router.get("/", response_model=List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
