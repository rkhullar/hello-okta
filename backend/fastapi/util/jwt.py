import datetime as dt
from dataclasses import dataclass, field
from typing import List, Optional, Union

import jwt
from cryptography.hazmat.primitives._serialization import (Encoding,
                                                           PublicFormat)
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from jwt import PyJWKClient


@dataclass
class TokenData:
    user_id: str
    email: str
    expiration: dt.datetime
    groups: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> 'TokenData':
        return cls(
            user_id=data['uid'],
            email=data['sub'],
            expiration=dt.datetime.fromtimestamp(data['exp']),
            groups=data.get('groups') or list()
        )


@dataclass
class TokenFactory:
    jwks_url: str
    algorithm: str = 'RS256'
    audience: str = 'api://default'

    def __post_init__(self):
        self.jwks_client = PyJWKClient(self.jwks_url)

    @staticmethod
    def public_key_to_string(key: RSAPublicKey) -> str:
        raw_text: bytes = key.public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo)
        return raw_text.decode('utf-8')

    def get_public_key(self, token: str, raise_error: bool = False, to_string: bool = False) -> Union[RSAPublicKey, str]:
        # NOTE: requires pyjwt[crypto] or cryptography
        try:
            token_header = jwt.get_unverified_header(token)
            signing_key = self.jwks_client.get_signing_key(token_header['kid'])
            public_key: RSAPublicKey = signing_key.key
            return self.public_key_to_string(public_key) if to_string else public_key
        except jwt.exceptions.PyJWTError as err:
            if raise_error:
                raise err

    def parse_token(self, token: str, raise_error: bool = False) -> Optional[TokenData]:
        # TODO: handle potential error?
        public_key = self.get_public_key(token)
        try:
            payload: dict = jwt.decode(token, key=public_key, algorithms=[self.algorithm], audience=self.audience)
            return TokenData.from_dict(payload)
        except jwt.exceptions.PyJWTError as err:
            if raise_error:
                raise err
