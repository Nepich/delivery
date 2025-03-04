import uvicorn

from settings import fastapi_settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def prepare_app():
    app = FastAPI(
        debug=fastapi_settings.DEBUG
    )
    app.add_middleware(
        CORSMiddleware(
            allow_origins=fastapi_settings.CORS_ALLOWED_ORIGINS
        )
    )
    return app
    
    
if __name__ == "__main__":
    app = prepare_app()
    uvicorn.run(app=app)
    