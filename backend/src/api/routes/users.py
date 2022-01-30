from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from src.core.dependencies import (
    check_permission,
    get_current_user,
    get_token_from_header,
)
from src.db.dependencies import get_user_repository
from src.db.repository.users import UserRepository
from src.schemas.users import (
    Permissions,
    User,
    UserInCreate,
    UserInUpdate,
    UserWithToken,
)

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
async def users(
    user_repository: UserRepository = Depends(get_user_repository),
    _: None = Depends(check_permission(Permissions.view)),
) -> List[User]:
    """
    Метод для получения всех пользователя
    """
    users = await user_repository.get_users()
    return [
        User(
            username=user.username,
            email=user.email,
            bio=user.bio,
            permission=user.permission,
        )
        for user in users
    ]


@router.post("/update", response_model=User, name="users:post-update-user")
async def update_user(
    user_update_fields: UserInUpdate,
    user_repository: UserRepository = Depends(get_user_repository),
    _: None = Depends(check_permission(Permissions.full)),
) -> User:
    """
    Метод для обновления пользователя
    """

    user = await user_repository.get_user_by_username(user_update_fields.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такого пользователя не существует",
        )

    updated_user = await user_repository.update_user(user_update_fields)

    return User(
        username=updated_user.username,
        email=updated_user.email,
        bio=updated_user.bio,
        permission=updated_user.permission,
    )


@router.post("/create", response_model=User, name="users:post-create-user")
async def create_user(
    user_create_fields: UserInCreate,
    user_repository: UserRepository = Depends(get_user_repository),
    _: None = Depends(check_permission(Permissions.full)),
) -> User:
    """
    Метод для создания пользователя
    """

    user = await user_repository.get_user_by_username(user_create_fields.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такой пользователь уже существует",
        )

    created_user = await user_repository.create_user(user_create_fields)

    return User(
        username=created_user.username,
        email=created_user.email,
        bio=created_user.bio,
        permission=created_user.permission,
    )


@router.delete("/delete", response_model=None, name="users:delete-user")
async def delete_user(
    username: str,
    user_repository: UserRepository = Depends(get_user_repository),
    _: None = Depends(check_permission(Permissions.full)),
) -> User:
    """
    Метод для удаления пользователя по его username
    """

    user = await user_repository.get_user_by_username(username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Такого пользователя не существует",
        )

    await user_repository.delete_user(username)
