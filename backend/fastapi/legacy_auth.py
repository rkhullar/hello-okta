import logging
from urllib.parse import urlencode

from httpx import HTTPStatusError
from okta import OktaClient

from config import Settings
from depends import get_base_url, get_okta_client, get_settings
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post('/token')
async def token(form_data: OAuth2PasswordRequestForm = Depends(), okta_client: OktaClient = Depends(get_okta_client), settings: Settings = Depends(get_settings)):
    try:
        return await okta_client.request_token(username=form_data.username, password=form_data.password, options=dict(
            state=settings.okta_app_state,
            redirect_uri=f'{settings.base_url}/authorization-code/callback'
        ))
    except HTTPStatusError:
        # TODO: consider adding custom exceptions or suppressing request_token
        raise HTTPException(status_code=401, detail='incorrect username or password')


@router.get('/login', response_class=RedirectResponse, status_code=302)
async def login(okta_client: OktaClient = Depends(get_okta_client), settings: Settings = Depends(get_settings)):
    query_params = dict(client_id=okta_client.client_id,
                        redirect_uri=f'{settings.base_url}/authorization-code/callback',
                        scope='openid',
                        state=settings.okta_app_state,
                        response_type='code',
                        response_mode='query')
    login_url = okta_client.authorization_url + '?' + urlencode(query_params)
    logging.info(login_url)
    return login_url


@router.get('/authorization-code/callback')
async def callback(code: str, okta_client: OktaClient = Depends(get_okta_client), base_url: str = Depends(get_base_url)):
    redirect_uri = f'{base_url}/authorization-code/callback'
    exchange = await okta_client.token_exchange(code=code, redirect_uri=redirect_uri)
    # TODO: redirect if using login flow instead of token flow?
    return {key: exchange[key] for key in ['token_type', 'access_token']}
