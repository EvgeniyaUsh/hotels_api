from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.exceptions import (
    HotelNotFoundHTTPException,
    ObjectNotFoundException,
    RoomNotFoundHTTPException,
    check_date_in_and_date_out,
)
from src.schemas.rooms import (
    RoomCreate,
    RoomCreateRequest,
    RoomPatch,
    RoomPatchRequest,
)

router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    check_date_in_and_date_out(date_from, date_to)
    return await db.rooms.get_filtered_by_date(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room_by_id(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await db.rooms.get_one(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException()


@router.post("/{hotel_id}/rooms")
async def create_room(
    hotel_id: int,
    db: DBDep,
    room_data: RoomCreateRequest = Body(),
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException()

    _room_data = RoomCreate(hotel_id=hotel_id, **room_data.model_dump())

    room = await db.rooms.create(_room_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomCreateRequest,
    db: DBDep,
):
    _room_data = RoomCreate(hotel_id=hotel_id, **room_data.model_dump())

    try:
        await db.rooms.update(_room_data, id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException()
    await db.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
)
async def partially_edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
    db: DBDep,
):
    _room_data = RoomPatch(
        hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True)
    )

    try:
        await db.rooms.update(_room_data, is_patch=True, id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException()
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}
