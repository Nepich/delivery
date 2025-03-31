from api.settings import fastapi_settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    debug=fastapi_settings.DEBUG
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=fastapi_settings.CORS_ALLOWED_ORIGINS
)