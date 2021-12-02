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

    ### wip

    def authenticate(self, username: str, password: str) -> dict:
        url = f'https://{self.domain}/api/v1/authn'
        payload = dict(
            username=username,
            password=password,
            options=dict(
                multiOptionalFactorEnroll=False,
                warnBeforePasswordExpired=False
            )
        )
        response = httpx.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def authorize(self, session_token: str) -> dict:
        url = self.metadata['authorization_endpoint']
        query_params = dict(
            client_id=self.client_id,
            scope='openid',
            sessionToken=session_token,
            state='ApplicationState',
            response_type='code',
            response_mode='query',
            redirect_uri='http://localhost:8000/authorization-code/callback'
        )
        response = httpx.get(url, params=query_params, follow_redirects=True)
        response.raise_for_status()
        return response.json()

    def request_token(self, username: str, password: str):
        auth_n_data = self.authenticate(username=username, password=password)
        auth_z_data = self.authorize(session_token=auth_n_data['sessionToken'])
        return auth_z_data
