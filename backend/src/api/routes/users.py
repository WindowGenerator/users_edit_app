from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.users import (
    UserWithToken,
    User,
    UserInUpdate,
    UserInCreate,
    Permissions,
)
from src.db.repository.users import fake_users_db
from src.core.security import get_current_user, check_permission, get_token_from_header

from typing import List


router = APIRouter(prefix="/users")


@router.get("/me", response_model=UserWithToken, name="users:get-current-user")
async def current_user(
    user: User = Depends(get_current_user),
    token: str = Depends(get_token_from_header),
    _: None = Depends(check_permission(Permissions.view)),
) -> UserWithToken:
    """
    Возвращает текущего пользователя
    """
    return UserWithToken(
        access_token=token,
        user=user,
    )


@router.get("/all", response_model=List[User], name="users:get-users")
async def users(_: None = Depends(check_permission(Permissions.view))) -> List[User]:
    """
    Метод для получения всех пользователя
    """
    return [
        User(username=user["username"], email=user["email"], bio=user["bio"])
        for _, user in fake_users_db.items()
    ]


@router.post("/update", response_model=User, name="users:post-update-user")
async def update_user(
    username: str,
    user_update_fields: UserInUpdate,
    _: None = Depends(check_permission(Permissions.full)),
) -> User:
    """
    Метод для обновления пользователя
    """
    if username not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такого пользователя не существует",
        )

    user_to_update = fake_users_db[username]
    user_to_update.update(user_update_fields)

    return User(**user_to_update)


@router.post("/create", response_model=User, name="users:post-create-user")
async def create_user(
    username: str,
    user_create_fields: UserInCreate,
    _: None = Depends(check_permission(Permissions.full)),
) -> User:
    """
    Метод для создания пользователя
    """
    if username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой пользователь уже существует",
        )

    fake_users_db[username] = user_create_fields.to_dict()

    return User(**fake_users_db[username])


@router.delete("/delete", response_model=None, name="users:delete-user")
async def delete_user(
    username: str, _: None = Depends(check_permission(Permissions.full))
) -> User:
    """
    Метод для удаления пользователя по его username
    """
    if username not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такого пользователя не существует",
        )

    del fake_users_db[username]
