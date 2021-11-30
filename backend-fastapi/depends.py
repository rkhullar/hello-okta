from config import Settings
from fastapi import Request


async def get_settings(request: Request) -> Settings:
    return request.app.extra['settings']
