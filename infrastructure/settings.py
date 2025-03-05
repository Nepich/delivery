from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    ADDRESS: str