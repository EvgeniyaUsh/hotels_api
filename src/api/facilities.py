from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.facilities import Facilities, FacilitiesCreate

router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("")
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

    return {"status": "OK", "data": facility}
