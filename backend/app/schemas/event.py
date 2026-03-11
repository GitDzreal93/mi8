"""Event-related schemas."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid


class EventBase(BaseModel):
    """Base event schema."""

    source: str
    title: str
    summary_en: Optional[str] = None
    summary_zh: Optional[str] = None
    event_type: Optional[str] = None
    importance: Optional[int] = None
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None
    geo_precision: Optional[str] = None
    actors: Optional[List[str]] = None
    equipment: Optional[List[str]] = None
    casualties: Optional[dict] = None
    tags: Optional[List[str]] = None
    confidence: Optional[float] = None
    event_time: Optional[datetime] = None


class EventCreate(EventBase):
    """Schema for creating an event."""

    canonical_event_id: Optional[str] = None
    raw_id: Optional[uuid.UUID] = None


class EventOut(EventBase):
    """Schema for event output."""

    id: uuid.UUID
    canonical_event_id: Optional[str] = None
    raw_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class EventFilter(BaseModel):
    """Schema for filtering events."""

    importance: Optional[int] = Field(None, ge=1, le=5)
    event_type: Optional[str] = None
    source: Optional[str] = None
    tags: Optional[str] = None
    q: Optional[str] = None
    hours: Optional[int] = Field(None, ge=1, le=168)
    min_confidence: Optional[float] = Field(None, ge=0, le=1)
    limit: int = Field(50, ge=1, le=200)
