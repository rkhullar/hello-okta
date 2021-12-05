import datetime as dt
from dataclasses import dataclass, field
from typing import List


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
            groups=data['groups']
        )