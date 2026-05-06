from datetime import date

from fastapi import APIRouter, Body, HTTPException, Query

from src.api.dependencies import DBDep, PaginationDep
from src.exceptions import (
    HotelHasRoomsHTTPException,
    HotelNotFoundHTTPException,
    ItemAlreadyExistsException,
    ObjectHasDependenciesException,
    ObjectNotFoundException,
)
from src.schemas.hotels import HotelCreate, HotelPatch
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Локация"),
    title: str | None = Query(None, description="Название отеля"),
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    return await HotelService(db).get_filtered_by_time(
        pagination=pagination,
        location=location,
        title=title,
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/{hotel_id}")
async def get_hotels_by_id(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel_by_id(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException()


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelCreate = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Сочи 5 звезд у моря",
                    "location": "Сочи, ул. Моря, 1",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Дубай У фонтана",
                    "location": "Дубай, ул. Шейха, 2",
                },
            },
        }
    ),
):
    try:
        hotel = await HotelService(db).create_hotel(hotel_data)
    except ItemAlreadyExistsException:
        raise HTTPException(status_code=409, detail="Hotel already exists.")
    await db.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int, hotel_data: HotelCreate, db: DBDep):
    try:
        await HotelService(db).put_hotel(hotel_id, hotel_data)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException()
    await db.commit()

    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить location, а можно title</h1>",
)
async def partially_edit_hotel(
    hotel_id: int,
    hotel_data: HotelPatch,
    db: DBDep,
):
    try:
        await HotelService(db).patch_hotel(hotel_id, hotel_data)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException()
    await db.commit()

    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    try:
        await HotelService(db).delete_hotel(hotel_id)
    except ObjectHasDependenciesException:
        raise HotelHasRoomsHTTPException()
    await db.commit()

    return {"status": "OK"}
