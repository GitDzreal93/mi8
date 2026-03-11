"""Data source models."""
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Date, Text, UniqueConstraint, JSON
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
