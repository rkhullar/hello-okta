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

    def request_token(self):
        metadata = self.metadata
        auth_url, token_url = metadata['authorization_endpoint'], metadata['token_endpoint']
        response = requests.get(auth_url, params=dict(
            client_id=self.client_id,
            response_type='code',
            redirect_uri='http://localhost:3000/api/auth/callback/okta',
            scope='openid',
            code_challenge='null'
        ))
        print(response)
        print(response.text)


if __name__ == '__main__':
    # define all sensitive values
    okta_domain = ''
    okta_client_id = ''
    okta_client_secret = ''
    test_username = ''
    test_password = ''

    okta = Okta(domain=okta_domain, client_id=okta_client_id, client_secret=okta_client_secret)
    #print(okta.metadata)
    okta.request_token()
