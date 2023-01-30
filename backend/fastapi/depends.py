from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer

from config import Settings
from okta import OktaClient
from schema import User
from util import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_settings(request: Request) -> Settings:
    return request.app.extra['settings']


async def get_base_url(settings: Settings = Depends(get_settings)) -> str:
    return settings.base_url


async def get_okta_client(request: Request) -> OktaClient:
    return request.app.extra['okta_client']


async def get_token_data(token: str = Depends(oauth2_scheme), okta_client: OktaClient = Depends(get_okta_client)) -> TokenData:
    return await okta_client.parse_token(token)


async def get_user(token_data: TokenData = Depends(get_token_data)) -> User:
    if not token_data:
        raise HTTPException(status_code=401, detail='could not validate token')
    return User(email=token_data.email, groups=token_data.groups)
