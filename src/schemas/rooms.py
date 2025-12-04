from pydantic import BaseModel, ConfigDict, Field


class RoomCreateRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomCreate(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class Room(RoomCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None


class RoomPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
