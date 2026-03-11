from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "mil-intel-api"
    environment: str = "local"
    debug: bool = True

    database_url: str = "postgresql+asyncpg://admin:Postgres%402026@localhost:5432/mi8"

    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-chat"
    deepseek_max_tokens: int = 512
    deepseek_rate_limit_qps: float = 0.5
    deepseek_daily_token_cap: int = 200_000
    deepseek_daily_request_cap: int = 5_000
    deepseek_timeout_seconds: int = 30

    gnews_api_key: str = ""
    newsapi_api_key: str = ""
    acled_api_key: str = ""
    rsshub_base: str = "https://rsshub.app"
    firms_api: str = "https://firms.modaps.eosdis.nasa.gov/api/"  # placeholder
    adsb_enabled: bool = False

    gnews_daily_limit: int = 100
    newsapi_daily_limit: int = 100
    acled_daily_limit: int = 1000
    rsshub_daily_limit: int = 1000
    firms_daily_limit: int = 200

    poll_interval_minutes: int = 30
    quota_stop_ratio: float = 0.8

    jwt_secret: str = "dev-secret"
    jwt_algorithm: str = "HS256"

    # Alert settings
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    alert_from: str = "alerts@milintel.local"
    alert_to: str = ""  # Comma-separated list of recipients
    slack_webhook_url: Optional[str] = None

    # Alert thresholds
    alert_min_importance: int = 4
    alert_quota_threshold: float = 0.8

settings = Settings()
