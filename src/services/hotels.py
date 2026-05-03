from datetime import date

from src.api.dependencies import PaginationDep
from src.exceptions import check_date_in_and_date_out
from src.schemas.hotels import HotelCreate, HotelPatch
from src.services.base import BaseService


class HotelsService(BaseService):
    async def get_filtered_by_time(
        self,
        pagination: PaginationDep,
        location: str | None,
        title: str | None,
        date_from: date,
        date_to: date,
    ):
        check_date_in_and_date_out(date_from, date_to)

        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

    async def get_hotel_by_id(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def create_hotel(self, data: HotelCreate):
        return await self.db.hotels.create(data)

    async def put_hotel(self, hotel_id: int, data: HotelCreate):
        return await self.db.hotels.update(data, id=hotel_id)

    async def patch_hotel(self, hotel_id: int, data: HotelPatch):
        return await self.db.hotels.update(data, id=hotel_id)

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
