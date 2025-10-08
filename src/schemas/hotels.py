from pydantic import BaseModel, ConfigDict, Field


class HotelCreate(BaseModel):
    title: str
    location: str


class Hotel(HotelCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class HotelPATCH(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)
