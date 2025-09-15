from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import settings


engine = create_async_engine(settings.DB_URL, echo=True)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

session = async_session_maker()


class Base(DeclarativeBase):
    pass


# from sqlalchemy import text
# async def func():
#     async with engine.begin() as conn:
#         res = await conn.execute(text("SELECT version()"))
#         print(res.fetchone())

# asyncio.run(func())
