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


class OktaSettings(BaseSettings):
    pass


class Settings(ProjectSettings, NetworkSettings, SecuritySettings, OktaSettings):
    pass
