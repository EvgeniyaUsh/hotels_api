from datetime import date

from sqlalchemy import func, select

from repositories.base import BaseRepository
from src.models.hotels import HotelOrm
from src.models.rooms import RoomOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelOrm
    schema = Hotel

    async def get_all(self, location, title, limit, offset):
        query = select(HotelOrm)
        if location:
            query = query.filter(
                func.lower(HotelOrm.location).contains(location.strip().lower())
            )
        if title:
            query = query.filter(
                func.lower(HotelOrm.title).contains(title.strip().lower())
            )
        query = query.limit(limit).offset(offset)

        result = await self.session.execute(query)

        return result.scalars().all()

    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomOrm.hotel_id)
            .select_from(RoomOrm)
            .filter(RoomOrm.id.in_(rooms_ids_to_get))
        )
        return await self.get_filtered(HotelOrm.id.in_(hotels_ids_to_get))
