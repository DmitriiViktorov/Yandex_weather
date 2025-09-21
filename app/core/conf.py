import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    days_length: int
    max_pressure_diff: int
    pressure_warning_raise: str
    pressure_warning_fall: str
    base_url: str
    timeout: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()
