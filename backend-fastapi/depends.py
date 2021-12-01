from fastapi import Depends, Request

from config import Settings
from okta import OktaClient


async def get_settings(request: Request) -> Settings:
    return request.app.extra['settings']


async def get_okta_client(settings: Settings = Depends(get_settings)) -> OktaClient:
    return OktaClient(domain=settings.okta_domain, client_id=settings.okta_client_id,
                      client_secret=settings.okta_client_secret)
