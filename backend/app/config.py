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
    # Public site origin for sitemap.xml / robots.txt (e.g. https://clintonage.com)
    site_url: str = "https://YOUR-DOMAIN.com"

    access_token_expire_minutes: int = 60 * 24
    algorithm: str = "HS256"

    @property
    def public_site_url(self) -> str:
        return self.site_url.rstrip("/")

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        """Normalize host Postgres URLs for SQLAlchemy + psycopg2.

        Render often provides postgres:// or postgresql://. Force the
        postgresql+psycopg2:// driver so the installed binary is used.
        """
        if not isinstance(value, str):
            return value
        if value.startswith("postgres://"):
            value = "postgresql://" + value[len("postgres://") :]
        if value.startswith("postgresql://"):
            value = "postgresql+psycopg2://" + value[len("postgresql://") :]
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
