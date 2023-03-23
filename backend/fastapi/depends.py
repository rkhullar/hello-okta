import os

from config import Settings
from fastapi import Depends, Request
from okta_flow import OktaAuthCodeBearer
from schema import User
from util import BearerAuth, async_httpx

''' legacy
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from util import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

async def get_token_data(token: str = Depends(oauth2_scheme), okta_client: OktaClient = Depends(get_okta_client)) -> TokenData:
    return await okta_client.parse_token(token)
    
async def get_user(token_data: TokenData = Depends(get_token_data)) -> User:
    if not token_data:
        raise HTTPException(status_code=401, detail='could not validate token')
    return User(email=token_data.email, groups=token_data.groups)
'''


async def get_settings(request: Request) -> Settings:
    return request.app.extra['settings']


async def get_base_url(settings: Settings = Depends(get_settings)) -> str:
    return settings.base_url


'''' doesn't show openapi logic
async def get_okta_flow(request: Request) -> OktaAuthCodeBearer:
    return request.app.extra['okta_flow']


async def get_access_token(request: Request, auth_scheme: OktaAuthCodeBearer = Depends(get_okta_flow)):
    return auth_scheme(request)


async def get_identity_token(auth_scheme: OktaAuthCodeBearer=Depends(get_okta_flow), access_token: str = Depends(get_access_token)) -> dict:
    response = await async_httpx(method='get', url=auth_scheme.userinfo_url, auth=BearerAuth(access_token))
    response.raise_for_status()
    return response.json()
'''

okta_host = os.environ['OKTA_DOMAIN']
auth_scheme = OktaAuthCodeBearer(domain=okta_host)


async def get_identity_token(access_token: str = Depends(auth_scheme)) -> dict:
    response = await async_httpx(method='get', url=auth_scheme.userinfo_url, auth=BearerAuth(access_token))
    response.raise_for_status()
    return response.json()


async def get_user(identity_token: dict = Depends(get_identity_token)) -> User:
    return User(email=identity_token['email'], groups=identity_token['groups'])
