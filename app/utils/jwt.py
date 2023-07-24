from jose import JWTError, jwt
from fastapi import Response
from datetime import datetime, timedelta, timezone

from ..schemas import Payload, TokenData
from ..config import settings


def create_jwt(payload):
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    return token


def is_valid_token(token):
    if not token:
        return False
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        user_id = payload["user"].get("id")
        if user_id is None:
            return False
        token_data = TokenData(refresh_token=payload["refresh_token"], **payload["user"])
    except JWTError:
        return False

    return token_data


def attach_access_token(res: Response, user: dict):
    access_token = create_jwt(payload=user)
    one_day = datetime.now(tz=timezone.utc) + timedelta(seconds=10)
    res.set_cookie(key="access_token", value=f"Bearer {access_token}", domain="localhost", httponly=True,
                   expires=one_day)


def attach_refresh_token(res: Response, user: dict, refresh_token: str):
    refresh_token_jwt = create_jwt(payload={"user": user, "refresh_token": refresh_token})

    longer_exp = datetime.now(tz=timezone.utc) + timedelta(days=1)
    res.set_cookie(key="refresh_token", value=f"Bearer {refresh_token_jwt}", httponly=True, domain="localhost",
                   expires=longer_exp)
