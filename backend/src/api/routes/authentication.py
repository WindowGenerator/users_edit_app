# noqa:WPS201
from fastapi import APIRouter, Depends, HTTPException

from src.schemas.users import UserInDB, UserInLogin, UserWithToken, User
from src.settings import get_app_settings, AppSettings
from src.db.repository.users import fake_users_db
from src.core.security import hash_password, create_user_token
from src.db.dependencies import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import User
from sqlalchemy import select


router = APIRouter(prefix="/auth")


@router.post("/login")
async def login(
    user_input: UserInLogin, 
    settings: AppSettings = Depends(get_app_settings),
    session: AsyncSession = Depends(get_session)
) -> UserWithToken:
    """
    Метод позволяющий залогинить пользвателя
    """
    
    
    result = await session.execute(select(User).where(User.username == user_input.username))
    user_dict = next(result)
    print(dict(user_dict))

    if not user_dict:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    user = UserInDB(**user_dict)
    hashed_password = hash_password(user_input.password)

    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_user_token(settings.secret_key, user.username)

    return UserWithToken(
        user=User(**user_dict),
        access_token=token
    )
