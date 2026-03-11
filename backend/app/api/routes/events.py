from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select, desc, or_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.database import get_session
from app.models.event import Event
from app.schemas.event import EventOut

router = APIRouter(prefix="/events", tags=["events"])

@router.get("", response_model=List[EventOut])
async def list_events(
    session: AsyncSession = Depends(get_session),
    importance: Optional[int] = Query(None, description="Minimum importance level (1-5)"),
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    source: Optional[str] = Query(None, description="Filter by source"),
    tags: Optional[str] = Query(None, description="Filter by tags (comma-separated)"),
    q: Optional[str] = Query(None, description="Search in title and summaries"),
    start_time: Optional[datetime] = Query(None, description="Start time filter"),
    end_time: Optional[datetime] = Query(None, description="End time filter"),
    hours: Optional[int] = Query(None, description="Last N hours (overrides start_time)"),
    min_confidence: Optional[float] = Query(None, description="Minimum confidence score"),
    limit: int = Query(50, le=200, description="Maximum number of results"),
):
    """List events with various filters."""
    stmt = select(Event).order_by(desc(Event.event_time))

    if hours:
        stmt = stmt.where(Event.event_time >= datetime.utcnow() - timedelta(hours=hours))
    elif start_time:
        stmt = stmt.where(Event.event_time >= start_time)

    if end_time:
        stmt = stmt.where(Event.event_time <= end_time)

    if importance:
        stmt = stmt.where(Event.importance >= importance)

    if event_type:
        stmt = stmt.where(Event.event_type == event_type)

    if source:
        stmt = stmt.where(Event.source == source)

    if min_confidence:
        stmt = stmt.where(Event.confidence >= min_confidence)

    if q:
        stmt = stmt.where(
            or_(
                Event.title.ilike(f"%{q}%"),
                Event.summary_en.ilike(f"%{q}%"),
                Event.summary_zh.ilike(f"%{q}%")
            )
        )

    if tags:
        tag_list = [t.strip() for t in tags.split(",")]
        for tag in tag_list:
            stmt = stmt.where(Event.tags.contains([tag]))

    stmt = stmt.limit(limit)
    rows = await session.scalars(stmt)
    return rows.all()

@router.get("/{event_id}", response_model=EventOut)
async def get_event(event_id: str, session: AsyncSession = Depends(get_session)):
    """Get a single event by ID."""
    row = await session.get(Event, event_id)
    if not row:
        raise HTTPException(status_code=404, detail="Event not found")
    return row

@router.get("/types/list")
async def list_event_types(session: AsyncSession = Depends(get_session)):
    """Get all unique event types."""
    stmt = select(Event.event_type).distinct().where(Event.event_type.isnot(None))
    rows = await session.scalars(stmt)
    return {"types": [r for r in rows.all() if r]}

@router.get("/sources/list")
async def list_event_sources(session: AsyncSession = Depends(get_session)):
    """Get all unique sources."""
    stmt = select(Event.source).distinct()
    rows = await session.scalars(stmt)
    return {"sources": rows.all()}
