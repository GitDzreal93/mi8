from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.core.security import get_current_user
from app.models.database import Event, RawItem
from app.services.ingest.aggregator import run_ingest

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/refresh")
async def trigger_refresh(
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """Manually trigger a data refresh. Requires authentication."""
    try:
        await run_ingest(session)
        return {"status": "success", "message": "Data refresh triggered"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Refresh failed: {str(e)}")

@router.post("/clear")
async def clear_data(
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    """Clear all events and raw items. Requires authentication."""
    # Delete all events first (due to foreign key)
    await session.execute(RawItem.__table__.delete())
    await session.execute(Event.__table__.delete())
    await session.commit()
    return {"status": "success", "message": "All data cleared"}

@router.get("/stats")
async def get_stats(session: AsyncSession = Depends(get_session)):
    """Get system statistics."""
    from sqlalchemy import select, func

    event_count = await session.scalar(select(func.count()).select_from(Event))
    raw_count = await session.scalar(select(func.count()).select_from(RawItem))

    # Get recent events by importance
    from datetime import datetime, timedelta
    recent_cutoff = datetime.utcnow() - timedelta(hours=24)
    recent_events = await session.scalar(
        select(func.count()).select_from(Event).where(Event.event_time >= recent_cutoff)
    )

    high_importance = await session.scalar(
        select(func.count()).select_from(Event).where(Event.importance >= 4)
    )

    return {
        "total_events": event_count or 0,
        "total_raw_items": raw_count or 0,
        "recent_events_24h": recent_events or 0,
        "high_importance_events": high_importance or 0,
    }
