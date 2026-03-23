from pydantic import BaseModel, ConfigDict, Field


class FacilitiesCreate(BaseModel):
    title: str


class Facilities(FacilitiesCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
