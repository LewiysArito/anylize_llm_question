from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from ipaddress import IPv4Address

class Analytic:
    pass

@dataclass(frozen=True)
class DataUserQuery(unsafe_hash=True):
    event_id: UUID
    model: str
    ip_address: IPv4Address
    raw_text: str
    timestamp: datetime