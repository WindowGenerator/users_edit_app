# noqa:WPS201
from hashlib import sha256

from fastapi.security import APIKeyHeader

HEADER_KEY = "Authorization"
AUTHORIZATION_API_KEY = APIKeyHeader(name=HEADER_KEY)


def hash_password(password: str) -> str:
    """
    Calculate hash from pass
    """
    return sha256(password.encode("utf-8")).hexdigest()


def create_user_token(secret_key: str, username: str) -> str:
    """
    Return fake user token
    """
    return username


def get_username_from_token(token: str) -> str:
    """
    Fake get username

    Хотелось бы заюзать криптографию для формирования нормальных токенов, но к сожалению низя(((
    """
    return token
