from repositories.base import BaseRepository
from src.models.bookings import BookingOrm
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingOrm
    schema = Booking
