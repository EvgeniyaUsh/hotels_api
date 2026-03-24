from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.facilities import Facilities, FacilitiesCreate
from src.init_redis import redis_manager

import json

router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("")
async def get_all_facilities(db: DBDep):
    facilities_from_cache = await redis_manager.get("facilities")
    if not facilities_from_cache:
        print("ИДУ В БАЗУ ДАННЫХ")
        facilities = await db.facilities.get_all()
        facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schemas)
        await redis_manager.set("facilities", facilities_json, 10)

        return facilities
    else:
        facilities_dicts = json.loads(facilities_from_cache)
        return facilities_dicts


@router.post("")
async def add_facility(
    user_id: UserIdDep,
    db: DBDep,
    title: str,
):

    facility = await db.facilities.create(FacilitiesCreate(title=title))
    await db.commit()

    return {"status": "OK", "data": facility}
