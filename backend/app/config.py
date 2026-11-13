from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "sqlite:///./portfolio.db"
    secret_key: str = "change-me-in-production"
    admin_username: str = "admin"
    admin_password: str = "changeme"

    mail_username: str = ""
    mail_password: str = ""
    mail_from: str = "noreply@example.com"
    mail_port: int = 587
    mail_server: str = "smtp.gmail.com"
    mail_to: str = ""
    mail_starttls: bool = True
    mail_ssl_tls: bool = False

    cors_origins: str = "http://localhost:8000,http://127.0.0.1:8000"

    access_token_expire_minutes: int = 60 * 24
    algorithm: str = "HS256"

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        """Render and some hosts provide postgres://; SQLAlchemy expects postgresql://."""
        if isinstance(value, str) and value.startswith("postgres://"):
            return "postgresql://" + value[len("postgres://") :]
        return value

    @field_validator("cors_origins", mode="before")
    @classmethod
    def strip_origins(cls, value: str) -> str:
        return value or ""

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def mail_configured(self) -> bool:
        return bool(self.mail_username and self.mail_password and self.mail_to)


@lru_cache
def get_settings() -> Settings:
    return Settings()
