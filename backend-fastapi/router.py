from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from config import Settings
from depends import get_okta_client, get_settings
from okta import OktaClient

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@router.get('/', response_class=RedirectResponse, status_code=302)
async def index():
    return 'docs'


@router.post('/token')
async def token(form_data: OAuth2PasswordRequestForm = Depends(), okta_client: OktaClient = Depends(get_okta_client)):
    return okta_client.request_token(username=form_data.username, password=form_data.password)


@router.get('/login', response_class=RedirectResponse, status_code=302)
async def login(okta_client: OktaClient = Depends(get_okta_client)):
    auth_url = okta_client.metadata['authorization_endpoint']
    query_params = dict(client_id=okta_client.client_id,
                        redirect_uri='http://localhost:8000/authorization-code/callback',
                        scope='openid',
                        state='ApplicationState',
                        response_type='code',
                        response_mode='query')
    login_url = auth_url + '?' + urlencode(query_params)
    print(login_url)
    return login_url


@router.get('/authorization-code/callback')
async def callback(code: str, okta_client: OktaClient = Depends(get_okta_client)):
    exchange = okta_client.token_exchange(code=code, redirect_uri='http://localhost:8000/authorization-code/callback')
    return {key: exchange[key] for key in ['token_type', 'access_token']}


@router.get('/profile')
async def profile(token: str = Depends(oauth2_scheme)):
    # TODO: parse token
    return {'token': token}


@router.get('/config')
async def config(settings: Settings = Depends(get_settings)):
    return settings
