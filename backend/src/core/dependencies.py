# noqa:WPS201
import json
from functools import partial
from hashlib import sha256
from typing import Callable, List, Optional

from fastapi import Depends, HTTPException, Security, Request
from fastapi.params import Security as SecurityParam
from fastapi.security import APIKeyHeader
from src.core.security import create_user_token, get_username_from_token
from src.db.dependencies import get_user_repository
from src.db.repository.users import UserRepository
from src.schemas.users import Permissions, User, UserFromDB
from src.settings import AppSettings, get_app_settings
from starlette import requests, status
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging


logger = logging.getLogger(__name__)


HEADER_KEY = "Authorization"
AUTHORIZATION_API_KEY = APIKeyHeader(name=HEADER_KEY)


def get_token_from_header(
    api_key: str = Security(AUTHORIZATION_API_KEY),
) -> str:
    return api_key


async def authorizantion(
    user_repository: UserRepository, token: str, secret_key: str
) -> None:
    username = get_username_from_token(token)

    if create_user_token(secret_key, username) != token:
        raise HTTPException(status_code=403, detail="Authorizantion error")

    user: UserFromDB = await user_repository.get_user_by_username(username)

    if not user:
        raise HTTPException(status_code=403, detail="Authorizantion error")

    return user


async def get_current_user(
    request: Request,
    token: str = Depends(get_token_from_header),
    settings: AppSettings = Depends(get_app_settings),
    user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    """
    Return current user
    """

    user = await authorizantion(user_repository, token, settings.secret_key)

    return User(
        username=user.username,
        email=user.email,
        bio=user.bio,
        permission=user.permission,
    )


def check_permission(
    permission_name: str,
) -> None:
    return partial(check_permissions_factory, permission_name)


def check_permissions_factory(
    permission_name: Permissions,
    user: User = Depends(get_current_user),
) -> None:

    if user.permission == Permissions.full:
        return

    if permission_name != user.permission:
        raise HTTPException(status_code=403, detail="Permission denied")
