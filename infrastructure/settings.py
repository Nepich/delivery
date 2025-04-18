from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class MQSettings(BaseSettings):
    QUEUE: str
    DESTINATION: str

    model_config = SettingsConfigDict(
        env_prefix="MQSettings__",
        env_file_encoding="utf-8",
        env_file=Path(__file__).parent.parent / ".env",
        extra="ignore"
    )


mq_settings = MQSettings()


class DBSettings(BaseSettings):
    DB_URL: str
    
    model_config = SettingsConfigDict(
        env_prefix="DBSettings__",
        env_file_encoding="utf-8",
        env_file=Path(__file__).parent.parent / ".env",
        extra="ignore"
    )
    
settings = DBSettings()