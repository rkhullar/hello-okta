import json
import os
from typing import List, Optional

from pydantic import BaseSettings


class ProjectSettings(BaseSettings):
    project: str = os.getenv('PROJECT', 'hello-okta')
    environment: Optional[str] = os.getenv('ENVIRONMENT')
    debug = bool(os.getenv('DEBUG', 0))


class NetworkSettings(BaseSettings):
    service_host: str = os.getenv('SERVICE_HOST', '0.0.0.0')
    service_port: int = int(os.getenv('SERVICE_PORT', '8000'))


class SecuritySettings(BaseSettings):
    secret_key: str = os.getenv('SECRET_KEY')
    allowed_origins: List[str] = json.loads(os.getenv('ALLOWED_ORIGINS', '[]'))


class OktaSettings(BaseSettings):
    okta_domain: str = os.getenv('OKTA_DOMAIN')
    okta_client_id: str = os.getenv('OKTA_CLIENT_ID')
    okta_client_secret: str = os.getenv('OKTA_CLIENT_SECRET')
    okta_app_state: str = 'ApplicationState'


class Settings(ProjectSettings, NetworkSettings, SecuritySettings, OktaSettings):
    # TODO: try to move properties to class level

    @property
    def base_url(self) -> str:
        return os.getenv('FASTAPI_URL') or f'http://localhost:{self.service_port}'
