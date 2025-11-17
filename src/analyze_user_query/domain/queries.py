from dataclasses import dataclass
from datetime import datetime
from ipaddress import IPv4Address
from uuid import UUID

class Query:
    pass

@dataclass
class DefineLanguage(Query):
    text: str

@dataclass
class DefineRegionByIp(Query):
    ip_address: IPv4Address | str

@dataclass
class AnalyzeUserQuery(Query):
    event_id: UUID
    model: str
    ip_address: IPv4Address
    raw_text: str
    timestamp: datetime