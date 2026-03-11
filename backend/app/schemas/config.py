"""Configuration schemas for API."""
from typing import Optional, Any, List
from pydantic import BaseModel, Field
from datetime import datetime


class ConfigBase(BaseModel):
    """Base configuration schema."""

    key: str = Field(..., description="Configuration key")
    value: Optional[Any] = Field(None, description="Configuration value")
    category: str = Field(..., description="Configuration category")
    description: Optional[str] = Field(None, description="Configuration description")
    is_sensitive: bool = Field(False, description="Whether the value is sensitive")


class ConfigCreate(ConfigBase):
    """Schema for creating a configuration."""

    pass


class ConfigUpdate(BaseModel):
    """Schema for updating a configuration."""

    value: Optional[Any] = Field(None, description="Configuration value")
    description: Optional[str] = Field(None, description="Configuration description")


class ConfigOut(ConfigBase):
    """Schema for configuration output."""

    id: str
    updated_at: datetime
    updated_by: Optional[str] = None

    class Config:
        from_attributes = True


class ConfigCategory(BaseModel):
    """Schema for configuration category."""

    category: str
    description: str
    configs: List[ConfigOut]


class ConfigBulkUpdate(BaseModel):
    """Schema for bulk updating configurations."""

    configs: List[dict] = Field(..., description="List of configurations to update")


class ConfigValidation(BaseModel):
    """Schema for configuration validation result."""

    valid: bool
    errors: List[str] = []


class ConfigReload(BaseModel):
    """Schema for configuration reload result."""

    success: bool
    message: str
    reloaded_keys: List[str] = []
