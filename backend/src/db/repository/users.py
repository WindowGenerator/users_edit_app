from hashlib import sha256
from typing import List, Optional

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.security import hash_password
from src.db.database import Base
from src.db.models import User
from src.schemas.users import UserFromDB, UserInCreate, UserInUpdate


def _alchemy_model2dict(model: Base):
    out_dict = {}
    for column in model.__table__.columns:
        out_dict[column.name] = getattr(model, column.name)

    return out_dict


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_user_by_username(self, username: str) -> Optional[UserFromDB]:
        result = await self._session.execute(
            select(User).where(User.username == username)
        )
        # FIXME(разобраться): await session.execute запускает неявную транзакцию????
        await self._session.commit()
        user = result.scalar()

        if user is None:
            return None

        return UserFromDB(**_alchemy_model2dict(user))

    async def get_users(self) -> List[UserFromDB]:
        result = await self._session.execute(select(User))
        users = list()

        for user in result.scalars():
            users.append(UserFromDB(**_alchemy_model2dict(user)))

        return users

    async def update_user(self, update_fields: UserInUpdate) -> Optional[UserFromDB]:
        update_fields_dict = update_fields.dict(
            exclude_none=True, exclude_unset=True, exclude={'password'}
        )
        if update_fields.password is not None:
            update_fields_dict['hashed_password'] = hash_password(
                update_fields.password
            )

        query = (
            update(User)
            .where(User.username == update_fields.username)
            .values(**update_fields_dict)
        )

        async with self._session.begin():
            await self._session.execute(query)

        return await self.get_user_by_username(update_fields.username)

    async def create_user(self, create_fields: UserInCreate) -> Optional[UserFromDB]:
        hashed_password = hash_password(create_fields.password)

        query = insert(User).values(
            username=create_fields.username,
            email=create_fields.email,
            bio=create_fields.bio,
            hashed_password=hashed_password,
            permission=create_fields.permission,
        )

        async with self._session.begin():
            await self._session.execute(query)

        return await self.get_user_by_username(create_fields.username)

    async def delete_user(self, username: str) -> None:
        query = delete(User).where(User.username == username)
        async with self._session.begin():
            await self._session.execute(query)
