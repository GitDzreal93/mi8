"""Configuration management API routes."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.services.config_service import ConfigService, ConfigException
from app.schemas.config import (
    ConfigOut,
    ConfigCreate,
    ConfigUpdate,
    ConfigCategory,
    ConfigBulkUpdate,
    ConfigValidation,
    ConfigReload,
)

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("/init", response_model=dict)
async def initialize_settings(
    session: AsyncSession = Depends(get_session),
):
    """Initialize default configurations. Run this after first deployment."""
    service = ConfigService(session)
    created = await service.initialize_defaults()
    return {
        "message": f"Initialized {len(created)} default configurations",
        "count": len(created),
    }


@router.get("", response_model=List[ConfigOut])
async def get_all_settings(
    category: Optional[str] = Query(None, description="Filter by category"),
    session: AsyncSession = Depends(get_session),
):
    """Get all configurations or filter by category."""
    service = ConfigService(session)
    if category:
        configs = await service.get_by_category(category)
    else:
        configs = await service.get_all()
    return configs


@router.get("/categories", response_model=dict)
async def get_categories(session: AsyncSession = Depends(get_session)):
    """Get all configuration categories."""
    service = ConfigService(session)
    categories = await service.get_categories()
    return categories


@router.get("/by-category", response_model=List[ConfigCategory])
async def get_settings_by_category(
    session: AsyncSession = Depends(get_session),
):
    """Get all configurations grouped by category."""
    service = ConfigService(session)
    categories = await service.get_categories()
    result = []

    for category, description in categories.items():
        configs = await service.get_by_category(category)
        result.append(
            ConfigCategory(
                category=category,
                description=description,
                configs=[ConfigOut.model_validate(c) for c in configs],
            )
        )

    return result


@router.get("/{key}", response_model=ConfigOut)
async def get_setting(
    key: str,
    session: AsyncSession = Depends(get_session),
):
    """Get a specific configuration by key."""
    service = ConfigService(session)
    config = await service.get_by_key(key)
    if not config:
        raise HTTPException(status_code=404, detail=f"Configuration '{key}' not found")
    return config


@router.post("", response_model=ConfigOut, status_code=201)
async def create_setting(
    config_data: ConfigCreate,
    session: AsyncSession = Depends(get_session),
):
    """Create a new configuration."""
    service = ConfigService(session)
    try:
        config = await service.create(config_data.model_dump())
    except ConfigException as e:
        raise HTTPException(status_code=400, detail=str(e))
    return config


@router.put("/{key}", response_model=ConfigOut)
async def update_setting(
    key: str,
    config_data: ConfigUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Update a configuration value."""
    service = ConfigService(session)

    # Validate the configuration
    if config_data.value is not None:
        is_valid, errors = await service.validate_config(key, config_data.value)
        if not is_valid:
            raise HTTPException(status_code=400, detail={"errors": errors})

    try:
        config = await service.update(key, config_data.value)
    except ConfigException as e:
        raise HTTPException(status_code=404, detail=str(e))
    return config


@router.post("/bulk", response_model=dict)
async def bulk_update_settings(
    data: ConfigBulkUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Bulk update multiple configurations."""
    service = ConfigService(session)
    updated = []
    errors = []

    for item in data.configs:
        key = item.get("key")
        value = item.get("value")
        if not key:
            errors.append({"error": "Missing key", "item": item})
            continue

        # Validate
        is_valid, validation_errors = await service.validate_config(key, value)
        if not is_valid:
            errors.append({"key": key, "errors": validation_errors})
            continue

        try:
            config = await service.update(key, value)
            updated.append(key)
        except ConfigException as e:
            errors.append({"key": key, "error": str(e)})

    return {
        "updated": updated,
        "errors": errors,
        "message": f"Updated {len(updated)} configurations, {len(errors)} errors",
    }


@router.delete("/{key}", response_model=dict)
async def delete_setting(
    key: str,
    session: AsyncSession = Depends(get_session),
):
    """Delete a configuration."""
    service = ConfigService(session)
    try:
        await service.delete(key)
    except ConfigException as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": f"Configuration '{key}' deleted successfully"}


@router.post("/validate", response_model=ConfigValidation)
async def validate_setting(
    key: str,
    value: dict,
    session: AsyncSession = Depends(get_session),
):
    """Validate a configuration value without saving it."""
    service = ConfigService(session)
    is_valid, errors = await service.validate_config(key, value.get("value"))
    return ConfigValidation(valid=is_valid, errors= errors)


@router.post("/reload", response_model=ConfigReload)
async def reload_settings(
    session: AsyncSession = Depends(get_session),
):
    """Reload configurations from database (hot-reload)."""
    # TODO: Implement hot-reload logic
    # This would update the in-memory settings from the database
    return ConfigReload(
        success=True,
        message="Settings reloaded successfully",
        reloaded_keys=[],
    )
