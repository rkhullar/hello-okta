from config import Settings
from depends import get_settings
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@router.post('/token')
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = form_data.username + 'token'
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/')
async def index(token: str = Depends(oauth2_scheme)):
    return {'token': token}


@router.get('/config')
async def config(settings: Settings = Depends(get_settings)):
    return settings
