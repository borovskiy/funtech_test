import os
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

SessionLocal = async_sessionmaker(
    bind=create_async_engine(os.environ.get("DATABASE_URL"), echo=False, ),
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


