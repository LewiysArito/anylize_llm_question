from dataclasses import dataclass
from datetime import datetime
from ipaddress import IPv4Address
from uuid import UUID

class Command:
    pass

@dataclass
class AnalyzeUserQuery(Command):
    event_id: UUID
    model: str
    ip_address: IPv4Address
    raw_text: str
    timestamp: datetime