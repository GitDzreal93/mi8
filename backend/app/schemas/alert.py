"""Alert-related schemas."""
from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel
import uuid


class AlertOut(BaseModel):
    """Schema for alert output."""

    id: uuid.UUID
    event_id: uuid.UUID
    channel: str
    payload: Optional[dict[str, Any]] = None
    sent: bool = False
    created_at: datetime

    class Config:
        from_attributes = True
