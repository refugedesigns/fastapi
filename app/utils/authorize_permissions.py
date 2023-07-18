from fastapi import HTTPException, status, Depends
from .jwt import is_valid_token
from .cookie_auth import oauth2_scheme


def get_current_user(auth_obj: dict = Depends(oauth2_scheme)):
    access_token = auth_obj.get("access_token")
    refresh_token = auth_obj.get("refresh_token")
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Invalid")
    if access_token is not None:
        user = is_valid_token(access_token)
        if not user:
            raise credentials_exception
        return user.dict()


class AuthorizePermissions:
    def __init__(self, *roles):
        self.roles = list(roles)

    def __call__(self, user=Depends(get_current_user)):
        user_role = user.get("role")
        if user_role not in self.roles:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized to access this route!")
        return True


admin_routes = AuthorizePermissions("admin", "moderator")
