"""SQLAlchemy database models."""
from datetime import datetime, date
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    Date,
    Boolean,
    JSON,
    Text,
    Float,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base


class Source(Base):
    """Data source configuration and status."""

    __tablename__ = "sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False)
    last_status = Column(String(20), default="unknown")
    last_message = Column(Text)
    last_polled_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )


class SourceUsage(Base):
    """Track daily API usage per source."""

    __tablename__ = "source_usage"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source = Column(String(50), nullable=False)
    day = Column(Date, nullable=False)
    count = Column(Integer, default=0)
    last_used_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    __table_args__ = (UniqueConstraint("source", "day", name="uq_source_day"),)


class RawItem(Base):
    """Raw data items from external sources."""

    __tablename__ = "raw_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source = Column(String(50), nullable=False)
    source_id = Column(String(200))
    title = Column(Text, nullable=False)
    url = Column(Text)
    published_at = Column(DateTime(timezone=True))
    content = Column(Text)
    raw = Column(JSON)
    hash_key = Column(String(64), index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    __table_args__ = (UniqueConstraint("source", "hash_key", name="uq_raw_source_hash"),)


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


class Alert(Base):
    """Alert notifications for high-importance events."""

    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"))
    channel = Column(String(20))  # email / slack
    payload = Column(JSON)
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)


class Feedback(Base):
    """User feedback on events."""

    __tablename__ = "feedback"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"))
    feedback = Column(Text, nullable=False)
    user = Column(String(100))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)


class Config(Base):
    """Application configuration settings stored in database."""

    __tablename__ = "configs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(JSON, nullable=True)
    category = Column(String(50), nullable=False, index=True)
    description = Column(Text)
    is_sensitive = Column(Boolean, default=False)
    updated_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    updated_by = Column(String(100))
