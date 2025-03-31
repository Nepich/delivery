from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    DB_URL: str
    
    
settings = DBSettings()