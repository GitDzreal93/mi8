from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Source

async def update_source_status(session: AsyncSession, name: str, status: str, message: str = ""):
    row = await session.scalar(select(Source).where(Source.name == name))
    if not row:
        row = Source(name=name)
        session.add(row)
        await session.flush()
    row.last_status = status
    row.last_message = message
    row.last_polled_at = datetime.utcnow()
