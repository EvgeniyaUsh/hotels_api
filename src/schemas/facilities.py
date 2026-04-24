from pydantic import BaseModel, ConfigDict


class FacilitiesCreate(BaseModel):
    title: str


class Facilities(FacilitiesCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
