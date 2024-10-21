import os
from typing import List

import ujson
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ###########
    # BACKEND #
    ###########
    SERVER_HOST: str = os.getenv("SERVER_HOST")
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT: int = os.getenv("BACKEND_PORT", 8000)

    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    VERSION: str = os.getenv("VERSION")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "very_secret_key")

    DEBUG: bool = os.getenv("DEBUG", True)

    DEFAULT_TIME_ZONE: str = os.getenv("DEFAULT_TIME_ZONE", "UTC")

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS")
    def parse_cors_origins(cls, value: str) -> List[str]:
        if isinstance(value, str):
            return ujson.loads(value)
        elif isinstance(value, (list, str)):
            return value

    class Config:
        case_sensitive = True


settings = Settings()
