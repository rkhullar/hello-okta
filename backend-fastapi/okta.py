from dataclasses import dataclass, field
from functools import cached_property
from typing import Dict, Optional

from util import async_httpx
from jwt import PyJWKClient
import jwt


@dataclass
class OktaClient:
    domain: str
    client_id: str
    client_secret: str = field(repr=False)

    @cached_property
    async def metadata(self) -> dict:
        response = await async_httpx(method='get', url=self.metadata_url)
        response.raise_for_status()
        return response.json()

    @property
    def metadata_url(self) -> str:
        return f'https://{self.domain}/oauth2/default/.well-known/openid-configuration'

    @property
    def authenticate_url(self) -> str:
        return f'https://{self.domain}/api/v1/authn'

    @property
    async def authorization_url(self) -> str:
        return (await self.metadata)['authorization_endpoint']

    @property
    async def token_url(self) -> str:
        return (await self.metadata)['token_endpoint']

    @property
    async def keys_url(self) -> str:
        return (await self.metadata)['jwks_uri']

    @cached_property
    async def jwks_client(self):
        return PyJWKClient(await self.keys_url)

    async def authenticate(self, username: str, password: str) -> dict:
        payload = dict(
            username=username,
            password=password,
            options=dict(
                multiOptionalFactorEnroll=False,
                warnBeforePasswordExpired=False
            )
        )
        response = await async_httpx(method='post', url=self.authenticate_url, json=payload)
        response.raise_for_status()
        return response.json()

    async def authorize(self, session_token: str, state: str, redirect_uri: str) -> dict:
        query_params = dict(
            client_id=self.client_id,
            scope='openid',
            sessionToken=session_token,
            state=state,
            response_type='code',
            response_mode='query',
            redirect_uri=redirect_uri
        )
        response = await async_httpx(method='get', url=await self.authorization_url,
                                     params=query_params, follow_redirects=True)
        response.raise_for_status()
        return response.json()

    async def token_exchange(self, code: str, redirect_uri: str) -> dict:
        payload = dict(grant_type='authorization_code', code=code, redirect_uri=redirect_uri)
        response = await async_httpx(method='post', url=await self.token_url,
                                     auth=(self.client_id, self.client_secret), data=payload)
        response.raise_for_status()
        return response.json()

    async def request_token(self, username: str, password: str, options: Dict[str, str]):
        auth_n_data = await self.authenticate(username=username, password=password)
        auth_z_data = await self.authorize(session_token=auth_n_data['sessionToken'],
                                           state=options['state'], redirect_uri=options['redirect_uri'])
        return auth_z_data

    async def _get_public_key(self, token: str) -> str:
        token_header = jwt.get_unverified_header(token)
        jwks_client = await self.jwks_client
        signing_key = jwks_client.get_signing_key(token_header['kid'])
        return signing_key.key

    async def parse_token(self, token: str, raise_error: bool = False) -> Optional[dict]:
        try:
            payload: dict = jwt.decode(token, key=self._get_public_key(token), algorithms=['RS256'], audience='api://default')
            return payload
        except jwt.exceptions.PyJWTError as err:
            if raise_error:
                raise err
