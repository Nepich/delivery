from pydantic_settings import BaseSettings


class GRPCSettings(BaseSettings):
    ADDRESS: str


class FastApiSettings(BaseSettings):
    DEBUG: bool
    CORS_ALLOWED_ORIGINS: list[str]
    
    
grpc_settings = GRPCSettings()
fastapi_settings = FastApiSettings()