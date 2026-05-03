from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from src.config import settings
from src.exceptions import (
    EmailNotRegisteredException,
    IncorrectPasswordException,
    ItemAlreadyExistsException,
)
from src.schemas.users import UserCreate, UserRequestCreate
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_jwt_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
        return encoded_jwt

    def get_hashed_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def decode_jwt_access_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Invalid token.")

    async def register_user(self, data: UserRequestCreate):
        hashed_password = self.get_hashed_password(data.password)
        new_user_data = UserCreate(
            email=data.email, hashed_password=hashed_password
        )
        try:
            await self.db.users.create(new_user_data)

        except IntegrityError as ex:
            raise ItemAlreadyExistsException from ex

        await self.db.commit()

    async def login_user(self, data: UserRequestCreate) -> str:
        user = await self.db.users.get_user_with_hashed_password(
            email=data.email
        )
        if not user:
            raise EmailNotRegisteredException
        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException
        access_token = self.encode_jwt_access_token({"user_id": user.id})
        return access_token

    async def get_one_or_none_user(
        self,
        user_id: int,
    ):
        return await self.db.users.get_one_or_none(id=user_id)
