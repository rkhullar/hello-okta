from dataclasses import dataclass, field

import requests


@dataclass
class Okta:
    domain: str
    client_id: str
    client_secret: str = field(repr=False)

    @property
    def metadata_url(self) -> str:
        return f'https://{self.domain}/oauth2/default/.well-known/openid-configuration'

    @property
    def metadata(self) -> dict:
        # TODO: cache
        response = requests.get(self.metadata_url)
        response.raise_for_status()
        return response.json()

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
        response = requests.post(url, json=payload)
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
        response = requests.get(url, params=query_params)
        print(response.text)

    def request_token(self, username: str, password: str):
        auth_n_data = self.authenticate(username=username, password=password)
        auth_z_data = self.authorize(session_token=auth_n_data['sessionToken'])
        print(auth_z_data)


if __name__ == '__main__':
    # define all sensitive values
    okta_domain = ''
    okta_client_id = ''
    okta_client_secret = ''
    test_username = ''
    test_password = ''

    okta = Okta(domain=okta_domain, client_id=okta_client_id, client_secret=okta_client_secret)
    # print(okta.metadata)
    okta.request_token(username=test_username, password=test_password)
