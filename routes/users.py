from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from db.dao import user as UserDao
from dto.user import UserCreate
from logic.auth.auth_db import authenticate_jwt

router = APIRouter()


@router.get("/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    user = await UserDao.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



@router.post("/")
async def get_all_users(offset: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)):
    response = await UserDao.get_users(db, offset, limit)
    return response


@router.get("/users-with-sims/")
async def get_users_with_sims(db: AsyncSession = Depends(get_session)):
    response = await UserDao.get_users_with_sims(db)
    return response


@router.post("/createUser")
async def create_user_handler(user: UserCreate, db: AsyncSession = Depends(get_session)):
    try:
        existing_user = await UserDao.get_user_by_username(db, user.username)
        if existing_user:
            return HTTPException(status_code=400, detail='username exists')
        created_user = await UserDao.create_user(db, user)
        return created_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



