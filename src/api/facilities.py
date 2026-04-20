from fastapi import APIRouter
from fastapi_cache.decorator import cache
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.facilities import FacilitiesCreate
from src.tasks.tasks import main_task


router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("")
@cache(expire=10)
async def get_all_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("")
async def add_facility(
    user_id: UserIdDep,
    db: DBDep,
    title: str,
):

    facility = await db.facilities.create(FacilitiesCreate(title=title))
    await db.commit()

    main_task.delay()

    return {"status": "OK", "data": facility}
