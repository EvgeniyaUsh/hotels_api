from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class RoomOrm(Base):
    __tablename__ = "room"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id"))
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]
