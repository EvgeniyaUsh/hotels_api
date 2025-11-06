from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep
from src.db import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserCreate, UserRequestCreate
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authorization and authentication"])


@router.post("/register")
async def register_user(
    data: UserRequestCreate,
):
    hashed_password = AuthService().get_hashed_password(data.password)
    new_user_data = UserCreate(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).create(new_user_data)
        await session.commit()

    return {"status": "OK"}


@router.post("/login")
async def login_user(
    data: UserRequestCreate,
    response: Response,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(
            email=data.email
        )
        if not user:
            raise HTTPException(status_code=401, detail="Incorrect email or password.")

        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect email or password.")
        access_token = AuthService().encode_jwt_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.get("/user")
async def get_user(
    user_id: UserIdDep,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
