from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, datetime
from app.core.database import get_session
from app.models.database import Source, SourceUsage
from app.core.config import settings

router = APIRouter()

@router.get("/health")
async def health():
    """Basic health check."""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@router.get("/sources/health")
async def get_sources_health(session: AsyncSession = Depends(get_session)):
    """Get all sources health status and quota information."""
    sources_stmt = select(Source)
    sources = await session.scalars(sources_stmt)
    sources_list = sources.all() if sources else []

    today = date.today()
    result = []

    for source in sources_list:
        # Get usage for today
        usage_stmt = select(SourceUsage).where(
            SourceUsage.source == source.name,
            SourceUsage.day == today
        )
        usage = await session.scalar(usage_stmt)

        # Get limits from config
        limit_map = {
            "gnews": settings.gnews_daily_limit,
            "newsapi": settings.newsapi_daily_limit,
            "acled": settings.acled_daily_limit,
            "rsshub": settings.rsshub_daily_limit,
            "firms": settings.firms_daily_limit,
        }
        limit = limit_map.get(source.name, 0)

        used = usage.count if usage else 0
        remaining = max(0, limit - used) if limit > 0 else None
        usage_percent = (used / limit * 100) if limit > 0 else None

        result.append({
            "name": source.name,
            "status": source.last_status,
            "message": source.last_message,
            "last_polled_at": source.last_polled_at.isoformat() if source.last_polled_at else None,
            "quota": {
                "limit": limit,
                "used": used,
                "remaining": remaining,
                "usage_percent": round(usage_percent, 2) if usage_percent else None,
                "stop_threshold": round(settings.quota_stop_ratio * 100, 2)
            }
        })

    return {"sources": result, "checked_at": datetime.utcnow().isoformat()}
