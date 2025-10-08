from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class UserOrm(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
