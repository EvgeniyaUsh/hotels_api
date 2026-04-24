from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base


class FacilitiesOrm(Base):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))


class RoomFacilitiesOrm(Base):
    __tablename__ = "room_facilities"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)

    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"))
    facilities_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))
