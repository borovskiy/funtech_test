from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from redis.asyncio import Redis

from app.core.settings import settings

SessionLocal = async_sessionmaker(
    bind=create_async_engine(settings.DATABASE_URL, echo=False, ),
    expire_on_commit=False,
)

async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def get_redis() -> Redis:
    return Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB_CACHE
    )
