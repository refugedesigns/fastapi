from fastapi import HTTPException, status, Depends, Response
from sqlalchemy.orm import Session
from .jwt import is_valid_token
from .cookie_auth import oauth2_scheme
from ..database import get_db
from .jwt import attach_access_token
from .. import models


def get_current_user(response: Response, auth_obj: dict = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    access_token = auth_obj.get("access_token")
    refresh_token = auth_obj.get("refresh_token")
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Invalid")
    if access_token is not None:
        user = is_valid_token(access_token)
        if not user:
            raise credentials_exception
        print("run access_token", access_token)
        return user.dict()
    elif refresh_token is not None:
        payload = is_valid_token(refresh_token)
        if not payload:
            raise credentials_exception
        existing_token = db.query(models.Token).filter(models.Token.refresh_token == payload.refresh_token,
                                                       models.Token.user_id == payload.id).first()
        if not existing_token or not existing_token.is_valid:
            raise credentials_exception
        user = {"id": payload.id, "email": payload.email, "role": payload.role}
        attach_access_token(response, user)
        return user
    else:
        raise credentials_exception


class AuthorizePermissions:
    def __init__(self, *roles):
        self.roles = list(roles)

    def __call__(self, user=Depends(get_current_user)):
        user_role = user.get("role")
        if user_role not in self.roles:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized to access this route!")
        return True


admin_routes = AuthorizePermissions("admin", "moderator")
