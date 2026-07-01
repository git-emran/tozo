from dataclasses import dataclass

from datetime import datetime


@dataclass
class Member:
    id: int
    email: str
    password_hash: str
    created: datetime
    email_verified: datetime | None
