from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep, PaginationDep
from src.schemas.hotels import HotelCreate, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Локация"),
    title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5

    results = await db.hotels.get_all(
        location, title, limit=per_page, offset=per_page * (pagination.page - 1)
    )
    return results


@router.get("/{hotel_id}")
async def get_hotels_by_id(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


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
    hotel = await db.hotels.create(hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int, hotel_data: HotelCreate, db: DBDep):
    await db.hotels.update(hotel_data, id=hotel_id)
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
    await db.hotels.update(hotel_data, is_patch=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}
