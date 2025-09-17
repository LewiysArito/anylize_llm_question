from dataclasses import dataclass
from datetime import datetime

class IntegrationEvent:
    pass

@dataclass
class UserQueryPublishedEvent(IntegrationEvent):
    event_id: str
    model: str
    ip_address: str
    raw_text: str
    timestamp: datetime