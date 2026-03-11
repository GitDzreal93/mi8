import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from .config import settings
from .models import Base

engine = create_async_engine(settings.database_url, echo=settings.debug)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    # First try to enable PostGIS extension in a separate transaction
    try:
        async with engine.begin() as conn:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        print("PostGIS extension enabled successfully")
    except Exception as e:
        print(f"PostGIS extension not available: {e}")
        print("Continuing without PostGIS - geo features will be disabled")

    # Then create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully")

async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

if __name__ == "__main__":
    asyncio.run(init_db())
