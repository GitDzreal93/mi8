"""Feedback model."""
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base


class Feedback(Base):
    """User feedback on events."""

    __tablename__ = "feedback"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"))
    feedback = Column(Text, nullable=False)
    user = Column(String(100))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
