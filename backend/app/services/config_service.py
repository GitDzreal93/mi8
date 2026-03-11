"""Configuration management service."""
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from datetime import datetime

from app.models.config import Config
from app.core.exceptions import MI8Exception
from app.core.config import settings as env_settings


class ConfigException(MI8Exception):
    """Configuration exception."""

    pass


class ConfigService:
    """Service for managing application configurations."""

    # Default configurations that should be initialized
    DEFAULT_CONFIGS = {
        # Database settings
        "database.url": {
            "value": env_settings.database_url,
            "category": "database",
            "description": "Database connection URL",
            "is_sensitive": True,
        },
        # DeepSeek LLM settings
        "llm.deepseek_api_key": {
            "value": env_settings.deepseek_api_key,
            "category": "llm",
            "description": "DeepSeek API key",
            "is_sensitive": True,
        },
        "llm.deepseek_base_url": {
            "value": env_settings.deepseek_base_url,
            "category": "llm",
            "description": "DeepSeek API base URL",
            "is_sensitive": False,
        },
        "llm.deepseek_model": {
            "value": env_settings.deepseek_model,
            "category": "llm",
            "description": "DeepSeek model name",
            "is_sensitive": False,
        },
        "llm.deepseek_max_tokens": {
            "value": env_settings.deepseek_max_tokens,
            "category": "llm",
            "description": "Maximum tokens per request",
            "is_sensitive": False,
        },
        "llm.deepseek_daily_token_cap": {
            "value": env_settings.deepseek_daily_token_cap,
            "category": "llm",
            "description": "Daily token limit",
            "is_sensitive": False,
        },
        "llm.deepseek_daily_request_cap": {
            "value": env_settings.deepseek_daily_request_cap,
            "category": "llm",
            "description": "Daily request limit",
            "is_sensitive": False,
        },
        # Data source API keys
        "sources.gnews_api_key": {
            "value": env_settings.gnews_api_key,
            "category": "sources",
            "description": "GNews API key",
            "is_sensitive": True,
        },
        "sources.newsapi_api_key": {
            "value": env_settings.newsapi_api_key,
            "category": "sources",
            "description": "NewsAPI.org API key",
            "is_sensitive": True,
        },
        "sources.acled_api_key": {
            "value": env_settings.acled_api_key,
            "category": "sources",
            "description": "ACLED API key",
            "is_sensitive": True,
        },
        "sources.rsshub_base": {
            "value": env_settings.rsshub_base,
            "category": "sources",
            "description": "RSSHub base URL",
            "is_sensitive": False,
        },
        "sources.firms_api": {
            "value": env_settings.firms_api,
            "category": "sources",
            "description": "NASA FIRMS API URL",
            "is_sensitive": False,
        },
        "sources.adsb_enabled": {
            "value": env_settings.adsb_enabled,
            "category": "sources",
            "description": "Enable ADS-B data source",
            "is_sensitive": False,
        },
        # Daily API limits
        "quota.gnews_daily_limit": {
            "value": env_settings.gnews_daily_limit,
            "category": "quota",
            "description": "GNews daily request limit",
            "is_sensitive": False,
        },
        "quota.newsapi_daily_limit": {
            "value": env_settings.newsapi_daily_limit,
            "category": "quota",
            "description": "NewsAPI daily request limit",
            "is_sensitive": False,
        },
        "quota.acled_daily_limit": {
            "value": env_settings.acled_daily_limit,
            "category": "quota",
            "description": "ACLED daily request limit",
            "is_sensitive": False,
        },
        "quota.rsshub_daily_limit": {
            "value": env_settings.rsshub_daily_limit,
            "category": "quota",
            "description": "RSSHub daily request limit",
            "is_sensitive": False,
        },
        "quota.firms_daily_limit": {
            "value": env_settings.firms_daily_limit,
            "category": "quota",
            "description": "FIRMS daily request limit",
            "is_sensitive": False,
        },
        # Polling settings
        "polling.interval_minutes": {
            "value": env_settings.poll_interval_minutes,
            "category": "polling",
            "description": "Data polling interval in minutes",
            "is_sensitive": False,
        },
        "polling.quota_stop_ratio": {
            "value": env_settings.quota_stop_ratio,
            "category": "polling",
            "description": "Stop polling when quota usage exceeds this ratio",
            "is_sensitive": False,
        },
        # JWT settings
        "auth.jwt_secret": {
            "value": env_settings.jwt_secret,
            "category": "auth",
            "description": "JWT signing secret",
            "is_sensitive": True,
        },
        "auth.jwt_expiration_days": {
            "value": env_settings.jwt_expiration_days,
            "category": "auth",
            "description": "JWT token expiration in days",
            "is_sensitive": False,
        },
        # Alert settings
        "alerts.smtp_host": {
            "value": env_settings.smtp_host,
            "category": "alerts",
            "description": "SMTP server host",
            "is_sensitive": False,
        },
        "alerts.smtp_port": {
            "value": env_settings.smtp_port,
            "category": "alerts",
            "description": "SMTP server port",
            "is_sensitive": False,
        },
        "alerts.smtp_user": {
            "value": env_settings.smtp_user,
            "category": "alerts",
            "description": "SMTP username",
            "is_sensitive": True,
        },
        "alerts.smtp_password": {
            "value": env_settings.smtp_password,
            "category": "alerts",
            "description": "SMTP password",
            "is_sensitive": True,
        },
        "alerts.from_email": {
            "value": env_settings.alert_from,
            "category": "alerts",
            "description": "Alert from email address",
            "is_sensitive": False,
        },
        "alerts.to_email": {
            "value": env_settings.alert_to,
            "category": "alerts",
            "description": "Alert to email address",
            "is_sensitive": False,
        },
        "alerts.slack_webhook_url": {
            "value": env_settings.slack_webhook_url,
            "category": "alerts",
            "description": "Slack webhook URL",
            "is_sensitive": True,
        },
        "alerts.min_importance": {
            "value": env_settings.alert_min_importance,
            "category": "alerts",
            "description": "Minimum importance level for alerts",
            "is_sensitive": False,
        },
        "alerts.quota_threshold": {
            "value": env_settings.alert_quota_threshold,
            "category": "alerts",
            "description": "Quota threshold for alerts",
            "is_sensitive": False,
        },
        # App settings
        "app.debug": {
            "value": env_settings.debug,
            "category": "app",
            "description": "Debug mode",
            "is_sensitive": False,
        },
        "app.environment": {
            "value": env_settings.environment,
            "category": "app",
            "description": "Application environment",
            "is_sensitive": False,
        },
    }

    # Category descriptions
    CATEGORY_DESCRIPTIONS = {
        "app": "Application settings",
        "database": "Database configuration",
        "llm": "Language Model settings (DeepSeek)",
        "sources": "Data source API keys and endpoints",
        "quota": "API quota limits for data sources",
        "polling": "Data polling configuration",
        "auth": "Authentication and authorization",
        "alerts": "Alert and notification settings",
    }

    def __init__(self, session: AsyncSession):
        self.session = session

    async def initialize_defaults(self) -> List[Config]:
        """Initialize default configurations if they don't exist."""
        created_configs = []
        for key, config_data in self.DEFAULT_CONFIGS.items():
            # Check if config exists
            result = await self.session.execute(
                select(Config).where(Config.key == key)
            )
            existing = result.scalar_one_or_none()

            if not existing:
                config = Config(
                    key=key,
                    value=config_data["value"],
                    category=config_data["category"],
                    description=config_data["description"],
                    is_sensitive=config_data["is_sensitive"],
                )
                self.session.add(config)
                created_configs.append(config)

        await self.session.commit()
        return created_configs

    async def get_all(self) -> List[Config]:
        """Get all configurations."""
        result = await self.session.execute(select(Config).order_by(Config.category, Config.key))
        return result.scalars().all()

    async def get_by_key(self, key: str) -> Optional[Config]:
        """Get configuration by key."""
        result = await self.session.execute(select(Config).where(Config.key == key))
        return result.scalar_one_or_none()

    async def get_by_category(self, category: str) -> List[Config]:
        """Get all configurations in a category."""
        result = await self.session.execute(
            select(Config)
            .where(Config.category == category)
            .order_by(Config.key)
        )
        return result.scalars().all()

    async def create(self, config_data: dict, updated_by: str = None) -> Config:
        """Create a new configuration."""
        # Check if key already exists
        existing = await self.get_by_key(config_data["key"])
        if existing:
            raise ConfigException(f"Configuration key '{config_data['key']}' already exists")

        config = Config(
            key=config_data["key"],
            value=config_data.get("value"),
            category=config_data["category"],
            description=config_data.get("description"),
            is_sensitive=config_data.get("is_sensitive", False),
            updated_by=updated_by,
        )
        self.session.add(config)
        await self.session.commit()
        await self.session.refresh(config)
        return config

    async def update(self, key: str, value: Any, updated_by: str = None) -> Config:
        """Update a configuration value."""
        config = await self.get_by_key(key)
        if not config:
            raise ConfigException(f"Configuration key '{key}' not found")

        config.value = value
        config.updated_by = updated_by
        config.updated_at = datetime.utcnow()

        await self.session.commit()
        await self.session.refresh(config)
        return config

    async def delete(self, key: str) -> bool:
        """Delete a configuration."""
        config = await self.get_by_key(key)
        if not config:
            raise ConfigException(f"Configuration key '{key}' not found")

        await self.session.execute(delete(Config).where(Config.key == key))
        await self.session.commit()
        return True

    async def get_categories(self) -> Dict[str, str]:
        """Get all configuration categories with descriptions."""
        # Get unique categories from database
        result = await self.session.execute(
            select(Config.category).distinct()
        )
        db_categories = set(result.scalars().all())

        # Merge with default categories
        categories = {**self.CATEGORY_DESCRIPTIONS}
        for cat in db_categories:
            if cat not in categories:
                categories[cat] = f"{cat.capitalize()} settings"

        return categories

    async def validate_config(self, key: str, value: Any) -> tuple[bool, List[str]]:
        """Validate a configuration value."""
        errors = []

        # Add specific validation logic here
        if key == "polling.interval_minutes":
            if not isinstance(value, int) or value < 1:
                errors.append("Polling interval must be a positive integer")
        elif key == "llm.deepseek_max_tokens":
            if not isinstance(value, int) or value < 1:
                errors.append("Max tokens must be a positive integer")
        elif key.endswith("api_key") or key.endswith("password"):
            if value and not isinstance(value, str):
                errors.append(f"{key} must be a string")
        elif "_enabled" in key or key.endswith("enabled"):
            if not isinstance(value, bool):
                errors.append(f"{key} must be a boolean")

        return len(errors) == 0, errors
