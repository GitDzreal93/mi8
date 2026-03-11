"""Database connection and session management."""
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from .config import settings

# Create async engine
engine = create_async_engine(settings.database_url, echo=settings.debug)

# Create session factory
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Base class for models
Base = declarative_base()


async def init_db() -> None:
    """Initialize database tables and extensions."""
    # Try to enable PostGIS extension in a separate transaction
    try:
        async with engine.begin() as conn:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        print("✅ PostGIS extension enabled successfully")
    except Exception as e:
        print(f"⚠️  PostGIS extension not available: {e}")
        print("   Continuing without PostGIS - geo features will be disabled")

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created successfully")


async def get_session() -> AsyncSession:
    """Get database session for dependency injection."""
    async with SessionLocal() as session:
        yield session


async def close_db() -> None:
    """Close database connections."""
    await engine.dispose()
