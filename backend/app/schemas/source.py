"""Source-related schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
import uuid


class RawItemIn(BaseModel):
    """Schema for creating a raw item."""

    source: str
    source_id: Optional[str] = None
    title: str
    url: Optional[str] = None
    published_at: Optional[datetime] = None
    content: Optional[str] = None
    raw: Optional[dict] = None


class RawItemOut(RawItemIn):
    """Schema for raw item output."""

    id: uuid.UUID
    hash_key: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SourceHealthOut(BaseModel):
    """Schema for source health status."""

    name: str
    status: str
    message: Optional[str] = None
    last_polled_at: Optional[datetime] = None
    quota: "QuotaInfo"


class QuotaInfo(BaseModel):
    """Schema for quota information."""

    limit: int
    used: int
    remaining: Optional[int] = None
    usage_percent: Optional[float] = None
    stop_threshold: float


class SourceUsageOut(BaseModel):
    """Schema for source usage statistics."""

    source: str
    day: str
    count: int

    class Config:
        from_attributes = True


# Update forward references
SourceHealthOut.model_rebuild()
