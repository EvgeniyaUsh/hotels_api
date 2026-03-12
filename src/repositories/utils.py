from datetime import date

from sqlalchemy import func, select

from src.models.bookings import BookingOrm
from src.models.rooms import RoomOrm


def rooms_ids_for_booking(
    date_from: date,
    date_to: date,
    hotel_id: int | None = None,
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
            RoomOrm.id.label("room_id"),
            (RoomOrm.quantity - func.coalesce(rooms_booked.c.rooms_count, 0)).label(
                "rooms_left"
            ),
        )
        .select_from(RoomOrm)
        .outerjoin(rooms_booked, rooms_booked.c.room_id == RoomOrm.id)
        .cte(name="rooms_available")
    )

    rooms_ids_by_hotel = select(RoomOrm.id).select_from(RoomOrm)

    if hotel_id:
        rooms_ids_by_hotel = rooms_ids_by_hotel.filter_by(hotel_id=hotel_id)

    query = (
        select(rooms_available.c.room_id)
        .select_from(rooms_available)
        .where(
            rooms_available.c.rooms_left > 0,
            rooms_available.c.room_id.in_(rooms_ids_by_hotel),
        )
    )
    return query
