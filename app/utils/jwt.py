from jose import JWTError, jwt
from fastapi import Response
from datetime import datetime, timedelta, timezone

from ..schemas import Payload, TokenData

SECRET_KEY = "8771107304ea807a9865e1784600d3f08a8bc25b360bba88b96f83d9c665"
ALGORITHM = "HS256"


def create_jwt(payload):
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def is_valid_token(token):
    if not token:
        return False
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id = payload.get("id")
        if user_id is None:
            return False

        token_data = TokenData(**payload)
    except JWTError:
        return False

    return token_data


def attach_access_token(res, user: dict):
    access_token = create_jwt(payload=user)
    one_day = datetime.now(tz=timezone.utc) + timedelta(seconds=10)
    res.set_cookie(key="access_token", value=f"Bearer {access_token}", domain="localhost", httponly=True,
                   expires=one_day)


def attach_refresh_token(res: Response, user: Payload, refresh_token: str):
    refresh_token_jwt = create_jwt(payload={"user": user, "refresh_token": refresh_token})

    longer_exp = datetime.utcnow() + timedelta(minutes=1)
    res.set_cookie(key="refresh_token", value=refresh_token_jwt, httponly=True, expires=longer_exp)
