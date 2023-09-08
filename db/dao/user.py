from sqlalchemy.orm import joinedload, defer
from db.models.user import User
from dto.user import UserCreate
from logic.utils.password import PasswordManager
from typing import Union, Dict, Optional, Any, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import Row, RowMapping
import asyncio


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    query = select(User).filter(User.id == user_id)
    result = await db.execute(query)
    return result.scalars().first() or False


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User] | bool:
    query = select(User).filter(User.username == username)
    result = await db.execute(query)
    return result.scalars().first() or False


async def get_users(db: AsyncSession, offset: int = 0, limit: int = 100) -> Sequence[Row | RowMapping | Any]:
    query = select(User).options(defer(User.password)).offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_users_with_sims(db: AsyncSession) -> Sequence[Row | RowMapping | Any]:
    query = select(User).options(joinedload(User.sims), defer(User.password))
    result = await db.execute(query)
    return result.scalars().all()


async def create_user(db: AsyncSession, user: UserCreate) -> Union[User, Dict[str, str]]:
    result = await asyncio.gather(db.execute(select(User).where(User.phone_number == user.phone_number)))

    existing_user = result[0].scalar()
    if existing_user:
        return {'error': 'phone_number exists'}
    hashed_password = await PasswordManager.hash_password(user.password)
    db_user = User(
        username=user.username,
        password=hashed_password,
        phone_number=user.phone_number
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
