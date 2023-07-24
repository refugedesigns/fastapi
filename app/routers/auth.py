from fastapi import HTTPException, status, Depends, APIRouter, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models
from ..utils.hash import hash_password, verify
from ..utils.jwt import attach_access_token, attach_refresh_token
import secrets

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)


@router.post("/signup", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    users = db.query(models.User).count()
    print(user)
    if users < 1:
        user.role = "admin"
    else:
        user.role = "user"
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"user with email {user.email} already exists.")

    hashed_pwd = hash_password(user.password)
    user.password = hashed_pwd

    new_user = models.User(**user.dict())  # unpack post object with key=value
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # retrieve new saved post from database
    return new_user


@router.post("/login", response_model=schemas.UserResponse)
def login_user(response: Response, credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Invalid Credentials")

    if not verify(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials")
    existing_refresh_token = db.query(models.Token).filter(models.Token.user_id == user.id).first()
    if not existing_refresh_token:
        token = secrets.token_hex(40)
        refresh_token = models.Token(user_id=user.id, refresh_token=token)
        db.add(refresh_token)
        db.commit()
        db.refresh(refresh_token)
        existing_refresh_token = refresh_token
    token_user = schemas.Payload(id=user.id, email=user.email, role=user.role)
    attach_access_token(response, token_user.dict())
    attach_refresh_token(response, token_user.dict(), existing_refresh_token.refresh_token)
    return user
