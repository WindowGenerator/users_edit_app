
import logging
import sys
from typing import Any, Dict, List, Tuple
import secrets
from pydantic import SecretStr, BaseSettings, Field


from functools import lru_cache
from typing import Dict, Type
import logging

logger = logging.getLogger(__name__)


class BaseFastApiSettings(BaseSettings):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "Users Edit App"
    version: str = "0.0.1"

    @property
    def fastapi_init_args(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }


class PostgresSettings(BaseSettings):
    pg_user: str = Field(env="PG_USER", default="postgres")
    pg_pass: str = Field(env="PG_PASSWORD", default="secret")
    pg_host: str = Field(env="PG_HOST", default="127.0.0.1")
    pg_database: str = Field(env="PG_DATABASE", default="users_db")

    @property
    def asyncpg_url(self) -> str:
        return f"postgresql+asyncpg://{self.pg_user}:{self.pg_pass}@{self.pg_host}:5432/{self.pg_database}"

    min_connection_count: int = 1
    max_connection_count: int = 10


# Наследование конечно зло, но так как это тестовое,    
# то можно им обойтись в угоду понятности конфигов
class AppSettings(BaseFastApiSettings, PostgresSettings):
    api_prefix: str = "/api"
    secret_key: SecretStr = secrets.token_hex(16)

    allowed_hosts: List[str] = ["*"]

    logging_level: int = logging.INFO

    class Config:
        validate_assignment = True


@lru_cache
def get_app_settings() -> AppSettings:
    logger.info("Loading config settings from the environment...")
    return AppSettings()
