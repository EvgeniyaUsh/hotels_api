from pydantic import BaseModel, ConfigDict, Field


class HotelCreate(BaseModel):
    title: str
    location: str


class Hotel(HotelCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class HotelPatch(BaseModel):
    title: str | None = None
    location: str | None = None
