import logging
from urllib.parse import urlencode

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from config import Settings
from depends import get_base_url, get_okta_client, get_settings, get_token_data
from okta import OktaClient
from util import TokenData, async_httpx

router = APIRouter()


@router.get('/', response_class=RedirectResponse, status_code=302)
async def index():
    return 'docs'


@router.post('/token')
async def token(form_data: OAuth2PasswordRequestForm = Depends(), okta_client: OktaClient = Depends(get_okta_client), settings: Settings = Depends(get_settings)):
    return await okta_client.request_token(username=form_data.username, password=form_data.password, options=dict(
        state=settings.okta_app_state,
        redirect_uri=f'{settings.base_url}/authorization-code/callback'
    ))


@router.get('/login', response_class=RedirectResponse, status_code=302)
async def login(okta_client: OktaClient = Depends(get_okta_client), settings: Settings = Depends(get_settings)):
    query_params = dict(client_id=okta_client.client_id,
                        redirect_uri=f'{settings.base_url}/authorization-code/callback',
                        scope='openid',
                        state=settings.okta_app_state,
                        response_type='code',
                        response_mode='query')
    login_url = await okta_client.authorization_url
    login_url += '?' + urlencode(query_params)
    logging.info(login_url)
    return login_url


@router.get('/authorization-code/callback')
async def callback(code: str, okta_client: OktaClient = Depends(get_okta_client), base_url: str = Depends(get_base_url)):
    redirect_uri = f'{base_url}/authorization-code/callback'
    exchange = await okta_client.token_exchange(code=code, redirect_uri=redirect_uri)
    return {key: exchange[key] for key in ['token_type', 'access_token']}


@router.get('/profile')
async def profile(token_data: TokenData = Depends(get_token_data)):
    return dict(token_data=token_data)


@router.get('/config')
async def config(settings: Settings = Depends(get_settings)):
    data = dict(settings)
    data['base_url'] = settings.base_url
    return data


@router.get('/hello')
async def hello(base_url: str = Depends(get_base_url)):
    result = list()
    result.append({'message': 'hello'})
    world_url = f'{base_url}/world'
    response = await async_httpx(method='get', url=world_url)
    response.raise_for_status()
    result.append(response.json())
    return result


@router.get('/world')
async def world():
    return {'message': 'world'}
