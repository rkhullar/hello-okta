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
