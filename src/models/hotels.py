from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class HotelOrm(Base):
    __tablename__ = "hotel"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str]
