from datetime import date

from fastapi import Query
from sqlalchemy import func, select

from repositories.base import BaseRepository
from src.db import engine
from src.models.bookings import BookingOrm
from src.models.rooms import RoomOrm
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
        rooms_booked = (
            select(BookingOrm.room_id, func.count().label("rooms_count"))
            .select_from(BookingOrm)
            .where(BookingOrm.date_from <= date_to, BookingOrm.date_to >= date_from)
            .group_by(BookingOrm.room_id)
            .cte(name="rooms_booked")
        )

        rooms_available = (
            select(
                self.model.id.label("room_id"),
                (
                    self.model.quantity - func.coalesce(rooms_booked.c.rooms_count, 0)
                ).label("rooms_left"),
            )
            .select_from(self.model)
            .outerjoin(rooms_booked, rooms_booked.c.room_id == self.model.id)
            .cte(name="rooms_available")
        )

        rooms_ids_by_hotel = (
            select(RoomOrm.id).select_from(RoomOrm).filter_by(hotel_id=hotel_id)
        )

        query = (
            select(rooms_available.c.room_id)
            .select_from(rooms_available)
            .where(
                rooms_available.c.rooms_left > 0,
                rooms_available.c.room_id.in_(rooms_ids_by_hotel),
            )
        )

        # выведет query запрос в sql стриле
        # print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        return await self.get_filtered(RoomOrm.id.in_(query))
