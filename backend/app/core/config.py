from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    # GitHub OAuth
    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str
    GITHUB_OAUTH_REDIRECT_URI: str = "http://localhost:8000/auth/callback"

    # App
    FRONTEND_CALLBACK_URL: str = "http://localhost:3000/auth/sign-in.html"
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    SECRET_KEY: str = "your-very-secure-random-secret-key-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database (MVP = SQLite)
    DB_NAME: str = "onelink_portfolio.db"
    DATABASE_URL: Optional[str] = None
    
    # Upload settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"
    ALLOWED_MEDIA_TYPES: list = [
        "image/png", "image/jpeg", "image/gif",
        "video/mp4", "video/webm"
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

    @property
    def database_url(self) -> str:
        return self.DATABASE_URL or f"sqlite:///./{self.DB_NAME}"


settings = Settings()