from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class GRPCSettings(BaseSettings):
    ADDRESS: str

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        env_file=Path(__file__).parent.parent / ".env",
        extra="ignore"
    )

class FastApiSettings(BaseSettings):
    DEBUG: bool
    CORS_ALLOWED_ORIGINS: list[str]

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        env_file=Path(__file__).parent.parent / ".env",
        extra="ignore"
    )
    
grpc_settings = GRPCSettings()
fastapi_settings = FastApiSettings()