from fastapi.security import OAuth2
from fastapi import HTTPException, status, Depends
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from .jwt import is_valid_token
from typing import Optional


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(self, tokenUrl: str, scheme_name: str = None, scopes: dict = None, auto_error: bool = True):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request):
        header_authorization: str = request.headers.get("Authorization")
        cookie_authorization: str = request.cookies.get("access_token")
        refresh_token_auth: str = request.cookies.get("refresh_token")

        header_scheme, header_param = get_authorization_scheme_param(header_authorization)
        cookie_scheme, cookie_param = get_authorization_scheme_param(cookie_authorization)
        refresh_scheme, refresh_param = get_authorization_scheme_param(refresh_token_auth)

        param = {}
        authorization = False
        scheme = None

        if header_scheme.lower() == "bearer":
            authorization = True
            scheme = header_scheme
            param = {"Authorization": header_param}

        if cookie_scheme.lower() == "bearer":
            authorization = True
            scheme = cookie_scheme
            param = {"access_token": cookie_param}

        if refresh_scheme.lower() == "bearer":
            authorization = True
            scheme = refresh_scheme
            param = {"refresh_token": refresh_param}

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authenticated")
            else:
                return None

        return param


oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="/login")


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
        print(user)
        user_role = user.get("role")
        if user_role not in self.roles:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized to access this route!")
        return True


authorize_permissions = AuthorizePermissions("admin", "moderator")