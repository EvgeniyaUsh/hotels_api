from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import (
    EmailNotRegisteredException,
    EmailNotRegisteredHTTPException,
    IncorrectPasswordException,
    IncorrectPasswordHTTPException,
    ItemAlreadyExistsException,
)
from src.schemas.users import UserRequestCreate
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authorization and authentication"])


@router.post("/register")
async def register_user(
    data: UserRequestCreate,
    db: DBDep,
):
    try:
        await AuthService(db).register_user(data)
    except ItemAlreadyExistsException:
        raise HTTPException(status_code=409, detail="User already exists.")

    return {"status": "OK"}


@router.post("/login")
async def login_user(
    data: UserRequestCreate,
    response: Response,
    db: DBDep,
):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(
    user_id: UserIdDep,
    db: DBDep,
):
    return await AuthService(db).get_one_or_none_user(user_id)


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
