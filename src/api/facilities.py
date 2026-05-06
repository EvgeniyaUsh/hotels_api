from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, UserIdDep
from src.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("")
@cache(expire=10)
async def get_all_facilities(db: DBDep):
    return await FacilityService(db).get_all_facilities()


@router.post("")
async def add_facility(
    user_id: UserIdDep,
    db: DBDep,
    title: str,
):
    facility = await FacilityService(db).add_facility(title)
    await db.commit()

    return {"status": "OK", "data": facility}
