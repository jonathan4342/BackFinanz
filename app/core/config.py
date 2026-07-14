"""Configuración central de la aplicación.

Carga variables de entorno con pydantic-settings. Un único punto de
verdad para la configuración (SRP): el resto de la app depende de este
objeto `settings` y no lee variables de entorno directamente.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # PostgreSQL
    POSTGRES_USER: str = "finanz"
    POSTGRES_PASSWORD: str = "finanz"
    POSTGRES_DB: str = "finanz"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    # URL explícita (tiene prioridad si se define; útil para tests con SQLite)
    DATABASE_URL: str | None = None

    # MongoDB (auditoría - opcional)
    MONGO_URL: str = "mongodb://localhost:27017"
    MONGO_DB: str = "finanz_audit"

    @property
    def database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
