from repositories.base import BaseRepository
from src.models.rooms import RoomOrm
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomOrm
    schema = Room
