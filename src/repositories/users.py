from repositories.base import BaseRepository
from src.models.users import UserOrm
from src.schemas.users import User


class UsersRepository(BaseRepository):
    model = UserOrm
    schema = User
