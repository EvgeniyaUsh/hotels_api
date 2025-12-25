from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomCreate, RoomCreateRequest, RoomPatch, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, db: DBDep):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room_by_id(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def create_room(
    hotel_id: int,
    db: DBDep,
    room_data: RoomCreateRequest = Body(),
):
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

    await db.rooms.update(_room_data, id=room_id)
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

    await db.rooms.update(_room_data, is_patch=True, id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_hotel(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}
