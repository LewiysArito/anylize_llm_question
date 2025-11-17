from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from ipaddress import IPv4Address

@dataclass(unsafe_hash=True, frozen=True)
class DataUserQuery:
    event_id: UUID
    model: str
    ip_address: IPv4Address
    raw_text: str
    timestamp: datetime

@dataclass(unsafe_hash=True, frozen=True)
class AnalyzedUserQuery:
    event_id: UUID
    text: str
    date: datetime
    themes: List[str]
    language_code: str
    country_code: Optional[str]
    user_ip: IPv4Address
    model_llm: str

@dataclass(unsafe_hash=True, frozen=True)
class AnalyzedUserQueryOrm:
    event_id: str
    text: str
    date: str
    themes: List[str]
    language_code: str
    country_code: Optional[str]
    user_ip: str
    model_llm: str