from datetime import date

from sqlalchemy import select

from src.models.bookings import BookingOrm
from src.repositories.base import BaseRepository
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingOrm
    schema = Booking

    async def get_bookings_with_today_checkin(self):
        query = select(BookingOrm).filter(BookingOrm.date_from == date.today())
        res = await self.session.execute(query)
        return [
            self.schema.model_validate(model) for model in res.scalars().all()
        ]
