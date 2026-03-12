"""Raw items API routes for data exploration."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime, timedelta

from app.core.database import get_session
from app.models.source import RawItem

router = APIRouter(prefix="/raw-items", tags=["raw-items"])


@router.get("")
async def list_raw_items(
    session: AsyncSession = Depends(get_session),
    source: Optional[str] = Query(None, description="Filter by source"),
    q: Optional[str] = Query(None, description="Search in title and content"),
    hours: Optional[int] = Query(None, description="Last N hours"),
    limit: int = Query(50, le=500, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
):
    """List raw items with filters and pagination."""
    stmt = select(RawItem).order_by(desc(RawItem.created_at))

    if source:
        stmt = stmt.where(RawItem.source == source)

    if hours:
        stmt = stmt.where(RawItem.created_at >= datetime.utcnow() - timedelta(hours=hours))

    if q:
        stmt = stmt.where(
            RawItem.title.ilike(f"%{q}%") | RawItem.content.ilike(f"%{q}%")
        )

    # Get total count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = await session.scalar(count_stmt) or 0

    # Apply pagination
    stmt = stmt.offset(offset).limit(limit)
    rows = await session.scalars(stmt)
    items = rows.all()

    return {
        "items": [
            {
                "id": str(item.id),
                "source": item.source,
                "source_id": item.source_id,
                "title": item.title,
                "url": item.url,
                "published_at": item.published_at.isoformat() if item.published_at else None,
                "content": item.content,
                "hash_key": item.hash_key,
                "created_at": item.created_at.isoformat() if item.created_at else None,
            }
            for item in items
        ],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/sources")
async def list_raw_item_sources(session: AsyncSession = Depends(get_session)):
    """Get all unique sources from raw items."""
    stmt = select(RawItem.source, func.count(RawItem.id).label("count")).group_by(RawItem.source)
    result = await session.execute(stmt)
    sources = [{"name": row.source, "count": row.count} for row in result.all()]
    return {"sources": sources}


@router.get("/stats")
async def raw_items_stats(session: AsyncSession = Depends(get_session)):
    """Get raw items statistics by source."""
    # Total count
    total = await session.scalar(select(func.count()).select_from(RawItem)) or 0

    # Count per source
    source_stmt = (
        select(
            RawItem.source,
            func.count(RawItem.id).label("count"),
            func.max(RawItem.created_at).label("latest"),
        )
        .group_by(RawItem.source)
        .order_by(desc("count"))
    )
    result = await session.execute(source_stmt)
    by_source = [
        {
            "source": row.source,
            "count": row.count,
            "latest": row.latest.isoformat() if row.latest else None,
        }
        for row in result.all()
    ]

    # Recent 24h count
    recent_cutoff = datetime.utcnow() - timedelta(hours=24)
    recent = await session.scalar(
        select(func.count()).select_from(RawItem).where(RawItem.created_at >= recent_cutoff)
    ) or 0

    return {
        "total": total,
        "recent_24h": recent,
        "by_source": by_source,
    }
