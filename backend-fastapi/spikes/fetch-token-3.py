from dataclasses import dataclass

import httpx
from util import load_secrets


@dataclass()
class ApiClient:
    base_url: str = 'http://localhost:8000'

    def test_token_flow(self, username: str, password: str):
        response = httpx.post(f'{self.base_url}/token', data=dict(username=username, password=password))
        response.raise_for_status()
        print(response.json()['access_token'])


if __name__ == '__main__':
    secrets = load_secrets()
    api_client = ApiClient()
    api_client.test_token_flow(username=secrets.test_username, password=secrets.test_password)
