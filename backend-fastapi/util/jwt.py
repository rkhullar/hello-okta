from dataclasses import asdict, dataclass, field
from typing import List
import datetime as dt


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
            expiration=data['exp'],
            groups=data['groups']
        )
