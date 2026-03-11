"""Common schemas used across the application."""
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel
import uuid


class HeatPoint(BaseModel):
    """Schema for heatmap data point."""

    lat: float
    lng: float
    weight: Optional[float] = 1.0


class FeedbackIn(BaseModel):
    """Schema for creating feedback."""

    event_id: uuid.UUID
    feedback: str
    user: Optional[str] = None


class FeedbackOut(FeedbackIn):
    """Schema for feedback output."""

    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


class SystemStats(BaseModel):
    """Schema for system statistics."""

    total_events: int
    total_raw_items: int
    recent_events_24h: int
    high_importance_events: int


class LoginRequest(BaseModel):
    """Schema for login request."""

    username: str
    password: str


class TokenResponse(BaseModel):
    """Schema for token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = None
