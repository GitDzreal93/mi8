from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.schemas.common import FeedbackIn, FeedbackOut
from app.models.database import Feedback, Event

router = APIRouter(prefix="/feedback", tags=["feedback"])

@router.post("", response_model=FeedbackOut)
async def submit_feedback(payload: FeedbackIn, session: AsyncSession = Depends(get_session)):
    """Submit feedback for an event."""
    # Verify event exists
    event = await session.get(Event, payload.event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    feedback = Feedback(
        event_id=payload.event_id,
        feedback=payload.feedback,
        user=payload.user
    )
    session.add(feedback)
    await session.commit()
    await session.refresh(feedback)

    return feedback

@router.get("/event/{event_id}")
async def get_event_feedback(event_id: str, session: AsyncSession = Depends(get_session)):
    """Get all feedback for an event."""
    stmt = select(Feedback).where(Feedback.event_id == event_id)
    rows = await session.scalars(stmt)
    return {"feedback": rows.all()}
