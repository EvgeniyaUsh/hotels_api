from src.schemas.facilities import FacilitiesCreate
from src.services.base import BaseService


class FacilityService(BaseService):
    async def get_all_facilities(self):
        return await self.db.facilities.get_all()

    async def add_facility(self, title: str):
        facility = FacilitiesCreate(title=title)
        return await self.db.facilities.create(facility)
