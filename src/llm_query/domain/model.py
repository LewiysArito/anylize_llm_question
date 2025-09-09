import dataclasses
from datetime import datetime
from uuid import UUID


@dataclasses(frozenset=True)
class UserQuery:
    id: UUID
    ip_address: str
    raw_text: str
    create_at: datetime