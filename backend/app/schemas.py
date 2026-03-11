from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel
import uuid

class EventCreate(BaseModel):
    source: str
    title: str
    summary_en: Optional[str]
    summary_zh: Optional[str]
    event_type: Optional[str]
    importance: Optional[int]
    location_lat: Optional[float]
    location_lng: Optional[float]
    geo_precision: Optional[str]
    actors: Optional[list]
    equipment: Optional[list]
    casualties: Optional[dict]
    tags: Optional[list]
    confidence: Optional[float]
    event_time: Optional[datetime]
    canonical_event_id: Optional[str]
    raw_id: Optional[uuid.UUID]

class EventOut(EventCreate):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class RawItemIn(BaseModel):
    source: str
    source_id: Optional[str]
    title: str
    url: Optional[str]
    published_at: Optional[datetime]
    content: Optional[str]
    raw: Optional[dict]

class RawItemOut(RawItemIn):
    id: uuid.UUID
    hash_key: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class HealthOut(BaseModel):
    source: str
    status: str
    last_polled_at: Optional[datetime]
    message: Optional[str]

class SourceUsageOut(BaseModel):
    source: str
    day: date
    count: int

class FeedbackIn(BaseModel):
    event_id: uuid.UUID
    feedback: str
    user: Optional[str]

class FeedbackOut(FeedbackIn):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True

class HeatPoint(BaseModel):
    lat: float
    lng: float
    weight: Optional[float] = 1.0
