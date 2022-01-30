# noqa:WPS201
from fastapi import APIRouter, Depends, HTTPException
from src.core.security import create_user_token, hash_password
from src.db.dependencies import get_user_repository
from src.db.repository.users import UserRepository
from src.schemas.users import User, UserFromDB, UserInLogin, UserWithToken
from src.settings import AppSettings, get_app_settings

router = APIRouter(prefix="/auth")


@router.post("/login")
async def login(
    user_input: UserInLogin,
    settings: AppSettings = Depends(get_app_settings),
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserWithToken:
    """
    Метод позволяющий залогинить пользвателя
    """

    user_from_db: UserFromDB = await user_repository.get_user_by_username(
        user_input.username
    )

    if not user_from_db:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    hashed_password = hash_password(user_input.password)

    if not hashed_password == user_from_db.hashed_password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_user_token(settings.secret_key, user_from_db.username)

    return UserWithToken(
        user=User(
            username=user_from_db.username,
            email=user_from_db.email,
            bio=user_from_db.bio,
            permission=user_from_db.permission,
        ),
        access_token=token,
    )
