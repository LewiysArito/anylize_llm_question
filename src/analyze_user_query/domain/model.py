from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from ipaddress import IPv4Address

@dataclass(frozen=True)
class DataUserQuery(unsafe_hash=True):
    event_id: UUID
    model: str
    ip_address: IPv4Address
    raw_text: str
    timestamp: datetime

@dataclass(frozen=True)
class AnalyzedUserQuery(unsafe_hash=True):
    event_id: UUID
    text: str
    date: datetime
    themes: List[str]
    language_code: str
    country_code: Optional[str]
    user_ip: IPv4Address
    model_llm: str