from dataclasses import dataclass, field

import httpx


@dataclass
class OktaClient:
    domain: str
    client_id: str
    client_secret: str = field(repr=False)

    @property
    def metadata_url(self) -> str:
        return f'https://{self.domain}/oauth2/default/.well-known/openid-configuration'

    @property
    def metadata(self) -> dict:
        # TODO: cache; look into httpx async or go back to requests
        response = httpx.get(self.metadata_url)
        response.raise_for_status()
        return response.json()

    def token_exchange(self, code: str, redirect_uri: str) -> dict:
        payload = dict(grant_type='authorization_code', code=code, redirect_uri=redirect_uri)
        response = httpx.post(self.metadata['token_endpoint'], auth=(self.client_id, self.client_secret), data=payload)
        response.raise_for_status()
        return response.json()
