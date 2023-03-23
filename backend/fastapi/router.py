from depends import get_base_url, get_user
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from schema import User
from util import async_httpx

router = APIRouter()


@router.get('/', response_class=RedirectResponse, status_code=302, include_in_schema=False)
async def index():
    return 'docs'


@router.get('/profile', response_model=User)
async def profile(user: User = Depends(get_user)):
    return user


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
