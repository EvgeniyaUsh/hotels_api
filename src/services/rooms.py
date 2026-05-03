from datetime import date

from src.exceptions import (
    check_date_in_and_date_out,
)
from src.schemas.rooms import (
    RoomCreate,
    RoomCreateRequest,
    RoomPatch,
    RoomPatchRequest,
)
from src.services.base import BaseService


class RoomService(BaseService):
    async def get_filtered_by_date(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        check_date_in_and_date_out(date_from, date_to)
        return await self.db.rooms.get_filtered_by_date(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to,
        )

    async def get_room_by_id(self, hotel_id: int, room_id: int):
        return await self.db.rooms.get_one(id=room_id, hotel_id=hotel_id)

    async def create_room(
        self,
        hotel_id: int,
        room_data: RoomCreateRequest,
    ):
        await self.db.hotels.get_one(id=hotel_id)
        room = RoomCreate(hotel_id=hotel_id, **room_data.model_dump())
        return await self.db.rooms.create(room)

    async def put_room(
        self,
        hotel_id: int,
        room_id: int,
        room_data: RoomCreateRequest,
    ):
        room = RoomCreate(hotel_id=hotel_id, **room_data.model_dump())
        await self.db.rooms.update(room, id=room_id)

    async def patch_room(
        self,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
    ):
        room = RoomPatch(
            hotel_id=hotel_id,
            **room_data.model_dump(exclude_unset=True),
        )
        await self.db.rooms.update(room, is_patch=True, id=room_id)

    async def delete_room(self, hotel_id: int, room_id: int):
        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
