from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    DB_URL: str
    
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        env_file=Path(__file__).parent.parent / ".env",
        extra="ignore"
    )
    
settings = DBSettings()