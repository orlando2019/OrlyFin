from __future__ import annotations

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="orlyfin-api", alias="APP_NAME")
    environment: str = Field(default="local", alias="ENVIRONMENT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    backend_host: str = Field(default="0.0.0.0", alias="BACKEND_HOST")
    backend_port: int = Field(default=8000, alias="BACKEND_PORT")
    api_v1_prefix: str = Field(default="/api/v1", alias="API_V1_PREFIX")

    cors_origins: list[str] = Field(default=["http://localhost:3000"], alias="CORS_ORIGINS")

    jwt_access_token_minutes: int = Field(default=15, alias="JWT_ACCESS_TOKEN_MINUTES")
    jwt_refresh_token_days: int = Field(default=7, alias="JWT_REFRESH_TOKEN_DAYS")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    jwt_access_secret_key: str = Field(default="change-me-access", alias="JWT_ACCESS_SECRET_KEY")
    jwt_refresh_secret_key: str = Field(default="change-me-refresh", alias="JWT_REFRESH_SECRET_KEY")
    jwt_access_cookie_name: str = Field(default="of_access_token", alias="JWT_ACCESS_COOKIE_NAME")
    jwt_refresh_cookie_name: str = Field(default="of_refresh_token", alias="JWT_REFRESH_COOKIE_NAME")
    jwt_cookie_secure: bool = Field(default=False, alias="JWT_COOKIE_SECURE")
    jwt_cookie_samesite: str = Field(default="lax", alias="JWT_COOKIE_SAMESITE")
    jwt_cookie_domain: str = Field(default="localhost", alias="JWT_COOKIE_DOMAIN")

    bootstrap_org_slug: str = Field(default="default-org", alias="BOOTSTRAP_ORG_SLUG")
    bootstrap_org_name: str = Field(default="Default Organization", alias="BOOTSTRAP_ORG_NAME")
    bootstrap_admin_email: str = Field(default="admin@orlyfin.local", alias="BOOTSTRAP_ADMIN_EMAIL")
    bootstrap_admin_password: str = Field(default="ChangeMe123!", alias="BOOTSTRAP_ADMIN_PASSWORD")

    attachments_storage_path: str = Field(default="./storage/attachments", alias="ATTACHMENTS_STORAGE_PATH")
    attachment_max_size_mb: int = Field(default=5, alias="ATTACHMENT_MAX_SIZE_MB")
    attachment_allowed_mime_types: list[str] = Field(
        default=["application/pdf", "image/png", "image/jpeg", "text/csv", "text/plain"],
        alias="ATTACHMENT_ALLOWED_MIME_TYPES",
    )

    alert_debt_due_days: int = Field(default=7, alias="ALERT_DEBT_DUE_DAYS")
    alert_pending_expense_threshold: int = Field(default=10, alias="ALERT_PENDING_EXPENSE_THRESHOLD")

    database_url: str = Field(
        default="postgresql+psycopg://orlyfin:orlyfin@localhost:5432/orlyfin",
        alias="DATABASE_URL",
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, list):
            return value
        return [item.strip() for item in value.split(",") if item.strip()]

    @field_validator("attachment_allowed_mime_types", mode="before")
    @classmethod
    def parse_attachment_allowed_mime_types(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, list):
            return value
        return [item.strip() for item in value.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
