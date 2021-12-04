from dataclasses import dataclass
from typing import Iterator

import httpx

from util import load_secrets


@dataclass
class BearerAuth(httpx.Auth):
    token: str

    def auth_flow(self, request: httpx.Request) -> Iterator[httpx.Request]:
        request.headers['authorization'] = f'Bearer {self.token}'
        yield request


@dataclass
class ApiClient:
    base_url: str = 'http://localhost:8000'

    def test_token_flow(self, username: str, password: str):
        response = httpx.post(f'{self.base_url}/token', data=dict(username=username, password=password))
        response.raise_for_status()
        access_token = response.json()['access_token']
        print(access_token)
        response = httpx.get(f'{self.base_url}/profile', auth=BearerAuth(access_token))
        response.raise_for_status()
        print(response.json())


if __name__ == '__main__':
    secrets = load_secrets()
    api_client = ApiClient()
    api_client.test_token_flow(username=secrets.test_username, password=secrets.test_password)
