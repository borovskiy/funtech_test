from contextlib import asynccontextmanager
import uvicorn

from fastapi import FastAPI, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_limiter.depends import RateLimiter

from starlette.middleware.cors import CORSMiddleware

from app.api import order_api, user_api

from app.core.access import limiter
from app.core.db_connector import get_redis
from app.workers.consumer_faststream import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await get_redis()
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    app.state.redis = redis
    yield
    await redis.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan, title="ORDERS", version="0.1.0",
                  dependencies=[Depends(RateLimiter(limiter=limiter))])

    # Настройка CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # Подключаем роутеры
    app.include_router(order_api.router, prefix="/api/v1")
    app.include_router(user_api.router, prefix="/api/v1")
    app.include_router(router)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("app.api_main:app", host="0.0.0.0", port=9000, reload=True)
