from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.exceptions import (
    HotelNotFoundHTTPException,
    ObjectHasDependenciesException,
    ObjectNotFoundException,
    RoomHasBookingsHTTPException,
    RoomNotFoundHTTPException,
)
from src.schemas.rooms import (
    RoomCreateRequest,
    RoomPatchRequest,
)
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    return await RoomService(db).get_filtered_by_date(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room_by_id(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await RoomService(db).get_room_by_id(hotel_id, room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException()


@router.post("/{hotel_id}/rooms")
async def create_room(
    hotel_id: int,
    db: DBDep,
    room_data: RoomCreateRequest = Body(),
):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException()
    await db.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomCreateRequest,
    db: DBDep,
):
    try:
        await RoomService(db).put_room(hotel_id, room_id, room_data)
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
    try:
        await RoomService(db).patch_room(hotel_id, room_id, room_data)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException()
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        await RoomService(db).delete_room(hotel_id, room_id)
    except ObjectHasDependenciesException:
        raise RoomHasBookingsHTTPException()
    await db.commit()
    return {"status": "OK"}
