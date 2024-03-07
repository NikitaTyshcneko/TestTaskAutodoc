from datetime import datetime, timedelta
from typing import Union, Any
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from app.settings import settings
from app.cruds import UserCruds
from app.database import db

token_auth_scheme = HTTPBearer()


def create_access_token(username: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "username": str(username)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET, settings.MY_ALGORITHMS)
    return encoded_jwt


def refresh_access_token(token: str, expires_delta: int = None) -> str:
    pyload_from_me = VerifyToken(token.credentials).verify_my()
    if pyload_from_me.get("status"):
        raise HTTPException(status_code=400, detail="token verification failed")
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "username": str(pyload_from_me.get("username"))}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET, settings.MY_ALGORITHMS)
    return encoded_jwt


async def get_username_from_token(token: str = Depends(token_auth_scheme)):
    pyload_from_me = VerifyToken(token.credentials).verify_my()
    if pyload_from_me.get("status"):
        raise HTTPException(status_code=400, detail="token verification failed")
    user_now = await UserCruds(db=db).get_user_by_username(str(pyload_from_me.get("username")))
    if str(pyload_from_me.get("username")) != str(user_now.username):
        raise HTTPException(status_code=400, detail="token verification failed")
    return pyload_from_me.get("username")


def set_up():
    config = {
        "MY_ALGORITHMS": settings.MY_ALGORITHMS,
        "SECRET": settings.SECRET
    }
    return config


class VerifyToken():
    """Does all the token verification using PyJWT"""

    def __init__(self, token):
        self.token = token
        self.config = set_up()

    def verify_my(self):
        try:
            payload = jwt.decode(
                self.token,
                self.config["SECRET"],
                algorithms=[self.config["MY_ALGORITHMS"]],
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

        return payload
