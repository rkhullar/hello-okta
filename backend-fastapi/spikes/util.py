from pathlib import Path
from dataclasses import dataclass
import json


@dataclass(frozen=True)
class Secrets:
    okta_domain: str
    okta_client_id: str
    okta_client_secret: str
    test_username: str
    test_password: str


def load_secrets() -> Secrets:
    path = Path(__file__).parent / 'local' / 'secrets.json'
    with path.open('r') as f:
        data = json.load(f)
        return Secrets(**data)
