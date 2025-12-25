from fastapi import APIRouter, Body, Query

from repositories.rooms import RoomsRepository
from src.api.dependencies import PaginationDep
from src.db import async_session_maker
from src.schemas.rooms import RoomCreate, RoomPatch, RoomCreateRequest, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        results = await RoomsRepository(session).get_filtered(hotel_id=hotel_id)
        return results


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room_by_id(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(
            id=room_id, hotel_id=hotel_id
        )


@router.post("/{hotel_id}/rooms")
async def create_room(
    hotel_id: int,
    room_data: RoomCreateRequest = Body(),
):
    _room_data = RoomCreate(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).create(_room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(hotel_id: int, room_id: int, room_data: RoomCreateRequest):
    _room_data = RoomCreate(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).update(_room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
)
async def partially_edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).update(_room_data, is_patch=True, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_hotel(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}
