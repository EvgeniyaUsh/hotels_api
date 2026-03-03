from datetime import date

from pydantic import BaseModel, ConfigDict


class BookingCreateRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingCreate(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int


class Booking(BookingCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
