from src.exceptions import check_date_in_and_date_out
from src.schemas.bookings import BookingCreate, BookingCreateRequest
from src.services.base import BaseService


class BookingService(BaseService):
    async def get_all_bookings(self):
        return await self.db.bookings.get_all()

    async def get_bookings_by_user(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def add_booking(
        self,
        user_id: int,
        booking_data: BookingCreateRequest,
    ):
        check_date_in_and_date_out(
            booking_data.date_from,
            booking_data.date_to,
        )
        room = await self.db.rooms.get_one(id=booking_data.room_id)
        booking = BookingCreate(
            user_id=user_id,
            price=room.price,
            **booking_data.model_dump(),
        )
        return await self.db.bookings.create(booking)
