from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException
from src.schemas.bookings import BookingCreateRequest
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Booking"])


@router.get("")
async def get_all_bookings(db: DBDep):
    return await BookingService(db).get_all_bookings()


@router.get("/me")
async def get_only_my_bookings(user_id: UserIdDep, db: DBDep):
    return await BookingService(db).get_bookings_by_user(user_id)


@router.post("")
async def add_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingCreateRequest,
):
    try:
        booking = await BookingService(db).add_booking(user_id, booking_data)
    except ObjectNotFoundException:
        raise HTTPException(
            status_code=400,
            detail="Room wasn't found.",
        )
    await db.commit()
    return {"status": "OK", "data": booking}
