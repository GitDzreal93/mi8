from datetime import date, datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import SourceUsage
from ..config import settings

LIMITS = {
    "gnews": settings.gnews_daily_limit,
    "newsapi": settings.newsapi_daily_limit,
    "acled": settings.acled_daily_limit,
    "rsshub": settings.rsshub_daily_limit,
    "firms": settings.firms_daily_limit,
}

async def can_fetch_source(session: AsyncSession, source: str) -> bool:
    limit = LIMITS.get(source, 0)
    if limit <= 0:
        return False
    today = date.today()
    usage = await session.scalar(select(SourceUsage).where(SourceUsage.source == source, SourceUsage.day == today))
    if not usage:
        return True
    return usage.count < int(limit * settings.quota_stop_ratio)

async def increment_source_usage(session: AsyncSession, source: str, count: int = 1):
    today = date.today()
    usage = await session.scalar(select(SourceUsage).where(SourceUsage.source == source, SourceUsage.day == today))
    if not usage:
        usage = SourceUsage(source=source, day=today, count=0)
        session.add(usage)
        await session.flush()
    usage.count += count
    usage.last_used_at = datetime.utcnow()
