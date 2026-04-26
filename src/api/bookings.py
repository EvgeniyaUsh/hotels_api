from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException
from src.schemas.bookings import BookingCreate, BookingCreateRequest

router = APIRouter(prefix="/bookings", tags=["Booking"])


@router.get("")
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_only_my_bookings(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def add_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingCreateRequest,
):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(
            status_code=400,
            detail="Room wasn't found.",
        )

    room_price: int = room.price
    _booking_data = BookingCreate(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )
    booking = await db.bookings.create(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}
