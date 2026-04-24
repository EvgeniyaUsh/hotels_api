from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base


class HotelOrm(Base):
    __tablename__ = "hotel"

    __table_args__ = (
        UniqueConstraint("title", "location", name="uq_hotel_title_location"),
    )

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str]
