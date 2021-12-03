import json
from pathlib import Path

from okta import OktaClient

if __name__ == '__main__':
    # read sensitive values
    secrets_path = Path(__file__).parent / 'local' / 'secrets.json'
    with secrets_path.open('r') as f:
        secrets = json.load(f)

    okta = OktaClient(domain=secrets['okta_domain'], client_id=secrets['okta_client_id'], client_secret=secrets['okta_client_secret'])
    # print(okta.metadata)
    result = okta.request_token(username=secrets['test_username'], password=secrets['test_password'])
    print(result['access_token'])
