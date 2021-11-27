from fastapi import FastAPI

from ..router import router as api_router
from .config import Settings


def create_app(settings: Settings, test: bool = False) -> FastAPI:
    app = FastAPI(settings=settings)
    app.include_router(api_router, prefix='/api')
    return app
