from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # PostgreSQL
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    DATABASE_URL: str | None

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
    REDIS_DB_CACHE:int

    # JWT / Auth
    JWT_SECRET: str
    JWT_ALG: str
    VERIFY_TOKEN_TTL_MIN: int

    class Config:
        env_file = "app/.env"
        env_file_encoding = "utf-8"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.DATABASE_URL:
            self.DATABASE_URL = (
                f"postgresql+asyncpg://{self.POSTGRES_USER}:"
                f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
                f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )
            print(self.DATABASE_URL)


settings = Settings()
