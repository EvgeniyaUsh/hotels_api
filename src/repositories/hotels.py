from sqlalchemy import func, select

from repositories.base import BaseRepository
from src.models.hotels import HotelOrm
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
