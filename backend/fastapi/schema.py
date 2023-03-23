from typing import List

from pydantic import BaseModel


class User(BaseModel):
    email: str
    groups: List[str]
