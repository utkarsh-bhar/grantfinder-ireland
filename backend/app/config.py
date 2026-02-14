"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """All settings loaded from environment / .env file."""

    # App
    APP_NAME: str = "GrantFinder Ireland"
    APP_URL: str = "https://grantfinder.ie"
    API_URL: str = "https://api.grantfinder.ie"
    ENVIRONMENT: str = "development"  # development | staging | production
    DEBUG: bool = True

    # Database (SQLite — uses /data/ path on Fly.io for persistence)
    DATABASE_URL: str = "sqlite:///./grantfinder.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # Auth / JWT
    JWT_SECRET: str = "CHANGE-ME-IN-PRODUCTION-use-a-random-256-bit-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_EXPIRY_MINUTES: int = 60
    JWT_REFRESH_EXPIRY_DAYS: int = 30

    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_PRICE_REPORT: str = ""
    STRIPE_PRICE_PREMIUM_MONTHLY: str = ""
    STRIPE_PRICE_PREMIUM_ANNUAL: str = ""

    # Anthropic (Claude API)
    ANTHROPIC_API_KEY: str = ""

    # AWS S3
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_S3_BUCKET: str = "grantfinder-reports"
    AWS_REGION: str = "eu-west-1"

    # Email
    SENDGRID_API_KEY: str = ""
    RESEND_API_KEY: str = ""
    FROM_EMAIL: str = "hello@grantfinder.ie"

    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""

    # Apple OAuth
    APPLE_CLIENT_ID: str = ""
    APPLE_TEAM_ID: str = ""
    APPLE_KEY_ID: str = ""

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "https://grantfinder.ie",
        "https://www.grantfinder.ie",
        "https://grantfinder-ireland.vercel.app",
        "https://frontend-sage-ten-80.vercel.app",
        "https://frontend-bhardwaju1995-5629s-projects.vercel.app",
    ]

    model_config = {"env_file": ".env", "case_sensitive": True}


@lru_cache()
def get_settings() -> Settings:
    return Settings()
