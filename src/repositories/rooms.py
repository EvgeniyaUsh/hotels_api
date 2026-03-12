from datetime import date

from fastapi import Query

from repositories.base import BaseRepository
from src.models.rooms import RoomOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomOrm
    schema = Room

    async def get_filtered_by_date(
        self,
        hotel_id: int,
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10"),
    ):
        query = rooms_ids_for_booking(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

        # выведет query запрос в sql стриле
        # print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        return await self.get_filtered(RoomOrm.id.in_(query))
