from contextlib import asynccontextmanager
import uvicorn

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.api import order_api, user_api
from redis.asyncio import Redis

from app.core.settings import settings
from app.workers.consumer_faststream import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB_CACHE
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    await redis.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan, title="ORDERS", version="0.1.0")
    app.include_router(order_api.router, prefix="/api/v1")
    app.include_router(user_api.router, prefix="/api/v1")
    app.include_router(router)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("app.api_main:app", host="0.0.0.0", port=9000, reload=True)