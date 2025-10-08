from fastapi import APIRouter
from passlib.context import CryptContext

from src.db import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserCreate, UserRequestCreate

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register_user(
    data: UserRequestCreate,
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserCreate(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).create(new_user_data)
        await session.commit()

    return {"status": "OK"}
