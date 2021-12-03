from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer

from config import Settings
from okta import OktaClient

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_settings(request: Request) -> Settings:
    return request.app.extra['settings']


async def get_base_url(settings: Settings = Depends(get_settings)) -> str:
    return settings.base_url


async def get_okta_client(settings: Settings = Depends(get_settings)) -> OktaClient:
    # TODO: move to app factory
    return OktaClient(domain=settings.okta_domain, client_id=settings.okta_client_id,
                      client_secret=settings.okta_client_secret)


async def get_token_data(token: str = Depends(oauth2_scheme), okta_client: OktaClient = get_okta_client):
    return await okta_client.parse_token(token)
