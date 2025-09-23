from dataclasses import dataclass
from datetime import datetime
from ipaddress import IPv4Address

class Command:
    pass

@dataclass
class UserQueryPublish(Command):
    model: str
    ip_address: IPv4Address
    raw_text: str
    created_at: datetime
