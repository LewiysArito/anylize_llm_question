from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

class Command:
    pass

@dataclass
class PublishData(Command):
    id: UUID
    model: str
    ip_address: str
    raw_text: str
    create_at: datetime
