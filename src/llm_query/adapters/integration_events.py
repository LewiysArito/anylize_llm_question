from dataclasses import dataclass

class IntegrationEvent:
    pass

@dataclass
class UserQueryPublishedEvent(IntegrationEvent):
    event_id: str
    model: str
    ip_address: str
    raw_text: str
    timestamp: str