from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.dao import user as UserDao
from dto.token import Token
from database import get_session

from logic.auth.auth_db import authenticate_jwt, JwtAuthenticator
from logic.auth.auth_ldap import authenticate_ldap

router = APIRouter()


@router.post('/getTokenLdap')
async def generate_token_ldap(username: str, password: str, db: AsyncSession = Depends(get_session)):
    is_auth = authenticate_ldap(username, password)
    if is_auth.get('error'):
        return HTTPException(401, detail=is_auth.get('error'))
    token = await JwtAuthenticator.create_access_token(username)
    return {
        'is_auth': True,
        'token': token,
        'token-type': 'bearer'
    }


@router.post("/getTokenServ")
async def generate_token(username: str, password: str, db: AsyncSession = Depends(get_session)):
    user = await UserDao.get_user_by_username(db, username)
    if user is None or False:
        return HTTPException(status_code=401, detail="Invalid username")
    status = await authenticate_jwt(password, user)
    return status


@router.post("/verifyToken")
async def protected_route(token: Token):
    response = await JwtAuthenticator.verify_token(token)
    return response
