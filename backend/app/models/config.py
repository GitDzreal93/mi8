"""Config model."""
from datetime import datetime
from sqlalchemy import Column, String, Boolean, Text, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base


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
