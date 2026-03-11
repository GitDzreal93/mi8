from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.database import get_session
from app.models.event import Event
from app.schemas.common import HeatPoint

router = APIRouter(prefix="/heatmap", tags=["heatmap"])


@router.get("", response_model=List[HeatPoint])
async def get_heatmap(
    session: AsyncSession = Depends(get_session),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    importance: Optional[int] = Query(None),
    limit: int = Query(1000, le=5000),
):
    """Get heatmap data as a list of points with weights."""
    stmt = select(Event).where(Event.location_lat.isnot(None)).where(Event.location_lng.isnot(None))

    if start_time:
        stmt = stmt.where(Event.event_time >= start_time)
    else:
        # Default to last 24 hours
        stmt = stmt.where(Event.event_time >= datetime.utcnow() - timedelta(hours=24))

    if end_time:
        stmt = stmt.where(Event.event_time <= end_time)

    if importance:
        stmt = stmt.where(Event.importance >= importance)

    stmt = stmt.order_by(desc(Event.event_time)).limit(limit)
    rows = await session.scalars(stmt)

    points = []
    for row in rows.all():
        weight = row.importance if row.importance else 1
        points.append(HeatPoint(lat=row.location_lat, lng=row.location_lng, weight=float(weight)))

    return points


@router.get("/geojson")
async def get_heatmap_geojson(
    session: AsyncSession = Depends(get_session),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    importance: Optional[int] = Query(None),
    limit: int = Query(1000, le=5000),
):
    """Get heatmap data as GeoJSON FeatureCollection."""
    stmt = select(Event).where(Event.location_lat.isnot(None)).where(Event.location_lng.isnot(None))

    if start_time:
        stmt = stmt.where(Event.event_time >= start_time)
    else:
        # Default to last 24 hours
        stmt = stmt.where(Event.event_time >= datetime.utcnow() - timedelta(hours=24))

    if end_time:
        stmt = stmt.where(Event.event_time <= end_time)

    if importance:
        stmt = stmt.where(Event.importance >= importance)

    stmt = stmt.order_by(desc(Event.event_time)).limit(limit)
    rows = await session.scalars(stmt)

    features = []
    for row in rows.all():
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row.location_lng, row.location_lat]
            },
            "properties": {
                "id": str(row.id),
                "title": row.title,
                "importance": row.importance or 1,
                "event_type": row.event_type,
                "source": row.source,
                "event_time": row.event_time.isoformat() if row.event_time else None,
                "summary_en": row.summary_en,
                "summary_zh": row.summary_zh,
                "actors": row.actors,
                "equipment": row.equipment,
                "confidence": row.confidence,
            }
        })

    return {
        "type": "FeatureCollection",
        "features": features
    }
