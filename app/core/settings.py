from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # PostgreSQL
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    DATABASE_URL: Optional[str] = None

    # Kafka
    KAFKA_HOST: str
    KAFKA_PORT: int

    # Ports
    POSTGRES_PORT: int
    KAFKA_PORT: int
    KAFKA_UI_PORT: int

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB_CACHE: int

    # JWT / Auth
    JWT_SECRET: str
    JWT_ALG: str
    VERIFY_TOKEN_TTL_MIN: int

    OAUTH_GOOGLE_CLIENT_ID: Optional[str]
    OAUTH_GOOGLE_CLIENT_SECRET: Optional[str]
    GOOGLE_APIS_TOKEN : str= "https://oauth2.googleapis.com/token"
    GOOGLE_AUTH_MAIN_LINK : str= "https://accounts.google.com/o/oauth2/v2/auth?"
    GOOGLE_AUTH_CALLBACK_LINK : str= "http://localhost:9000/api/v1/user_auth/auth/google/callback"

    class Config:
        env_file = "app/not_compose.env"
        env_file_encoding = "utf-8"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.DATABASE_URL:
            self.DATABASE_URL = (
                f"postgresql+asyncpg://{self.POSTGRES_USER}:"
                f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
                f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )


settings = Settings()
