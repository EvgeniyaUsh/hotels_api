import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI

sys.path.append(str(Path(__file__).parent.parent))

from src.api.auth import router as router_auth
from src.api.bookings import router as router_bookings
from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.api.facilities import router as router_facilities
from src.init_redis import redis_manager

from contextlib import asynccontextmanager


@asynccontextmanager
async def redis_lifespan(app: FastAPI):
    await redis_manager.connect()
    yield
    await redis_manager.close()


app = FastAPI(lifespan=redis_lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
