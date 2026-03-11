"""Event model."""
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Float, JSON, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base


class Event(Base):
    """Structured military events."""

    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    canonical_event_id = Column(String(64), index=True)
    source = Column(String(50), nullable=False)
    title = Column(Text, nullable=False)
    summary_en = Column(Text)
    summary_zh = Column(Text)
    event_type = Column(String(50))
    importance = Column(Integer)
    location_lat = Column(Float)
    location_lng = Column(Float)
    # Note: PostGIS geometry column disabled when PostGIS extension is not available
    # location = Column(Geometry(geometry_type='POINT', srid=4326, spatial_index=True))
    geo_precision = Column(String(20))
    actors = Column(JSON)
    equipment = Column(JSON)
    casualties = Column(JSON)
    tags = Column(JSON)
    confidence = Column(Float)
    event_time = Column(DateTime(timezone=True))
    raw_id = Column(UUID(as_uuid=True), ForeignKey("raw_items.id"))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
