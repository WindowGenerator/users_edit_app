# noqa:WPS201
from typing import Callable, Optional, List
import json
from functools import partial
from fastapi import Depends, HTTPException, Security
from fastapi.params import Security as SecurityParam
from fastapi.security import APIKeyHeader
from starlette import requests, status
from starlette.exceptions import HTTPException as StarletteHTTPException

from hashlib import sha256
from src.schemas.users import User, Permissions
from src.settings import get_app_settings, AppSettings
from src.db.repository.users import fake_users_db

HEADER_KEY = "Authorization"
AUTHORIZATION_API_KEY = APIKeyHeader(name=HEADER_KEY)


def hash_password(password: str) -> str:
    """Возвращает хэш от пароля"""
    return sha256(password.encode("utf-8")).hexdigest()


def get_token_from_header(
    api_key: str = Security(AUTHORIZATION_API_KEY),
) -> str:
    return api_key


def create_user_token(secret_key: str, username: str) -> str:
    return username


def _get_username_from_token(token: str) -> str:
    return token


async def get_current_user(
    token: str = Depends(get_token_from_header),
    settings: AppSettings = Depends(get_app_settings),
) -> User:

    username = _get_username_from_token(token)

    if create_user_token(settings.secret_key, username) != token:
        raise HTTPException(status_code=403, detail="Authorizantion error")

    return User(**fake_users_db[username])


def check_permission(
    permission_name: str,
) -> None:
    return partial(check_permissions_factory, permission_name)


def check_permissions_factory(
    permission_name: Permissions,
    token: str = Depends(get_token_from_header),
    settings: AppSettings = Depends(get_app_settings),
) -> None:
    username = _get_username_from_token(token)

    if create_user_token(settings.secret_key, username) != token:
        raise HTTPException(status_code=403, detail="Authorizantion error")

    user = fake_users_db[username]

    if permission_name not in user["permission"]:
        raise HTTPException(status_code=403, detail="Permission denied")
