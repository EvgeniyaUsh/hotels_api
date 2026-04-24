from src.config import settings
from src.lifespans.redis_lifespan import RedisManager

redis_manager = RedisManager(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
)
