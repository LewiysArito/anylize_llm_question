from dataclasses import dataclass
from datetime import datetime
from ipaddress import IPv4Address
from typing import List, Optional
from uuid import UUID

class Command:
    pass

@dataclass(unsafe_hash=True, frozen=True)
class SaveUserQuery(Command):
    event_id: UUID
    text: str
    date: datetime
    themes: List[str]
    language_code: str
    country_code: Optional[str]
    user_ip: IPv4Address
    model_llm: str