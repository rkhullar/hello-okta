from dataclasses import dataclass
from typing import Iterator

import httpx

from util import load_secrets


@dataclass
class SSWSAuth(httpx.Auth):
    token: str

    def auth_flow(self, request: httpx.Request) -> Iterator[httpx.Request]:
        request.headers['authorization'] = f'SSWS {self.token}'
        yield request


@dataclass
class OktaClient:
    domain: str
    api_key: str

    def iter_apps(self) -> Iterator[dict]:
        url = f'https://{self.domain}/api/v1/apps'
        response = httpx.get(url, auth=SSWSAuth(self.api_key))
        response.raise_for_status()
        yield from response.json()

    def find_app(self, name: str) -> dict:
        for app in self.iter_apps():
            if app['label'] == name:
                return app

    def set_app_profile(self, app: dict, data: dict):
        # https://developer.okta.com/docs/reference/api/apps/#update-application-level-profile-attributes
        app = dict(app)
        app_id = app['id']
        for key in 'id', 'created', 'lastUpdated':
            app.pop(key)
        app['profile'] = data
        url = f'https://{self.domain}/api/v1/apps/{app_id}'
        response = httpx.put(url, json=app, auth=SSWSAuth(self.api_key))
        return response


if __name__ == '__main__':
    import json
    secrets = load_secrets()
    okta_client = OktaClient(domain=secrets.okta_domain, api_key=secrets.okta_api_key)
    app = okta_client.find_app('Hello World')
    print(json.dumps(app, indent=4, sort_keys=True))
    # okta_client.set_app_profile(app, data={'group_prefix': 'nydev-example'})
