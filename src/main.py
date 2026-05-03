import asyncio
import logging
import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

sys.path.append(str(Path(__file__).parent.parent))

from contextlib import asynccontextmanager

from src.api.auth import router as router_auth
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.hotels import router as router_hotels
from src.api.images import router as router_images
from src.api.rooms import router as router_rooms
from src.init_redis import redis_manager
from src.tasks.periodic_task import run_send_email_regularly  # noqa: F401

logging.basicConfig(level=logging.DEBUG)


@asynccontextmanager
async def redis_lifespan(app: FastAPI):
    # Инициализация Redis при запуске приложения
    # asyncio.create_task(run_send_email_regularly())
    await redis_manager.connect()
    FastAPICache.init(
        RedisBackend(redis_manager._redis), prefix="fastapi-cache"
    )
    yield
    logging.info("FastAPI cache initialized")
    # Закрытие соединения с Redis при завершении приложения
    await redis_manager.close()


app = FastAPI(lifespan=redis_lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)
app.include_router(router_images)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
