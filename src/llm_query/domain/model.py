import dataclasses
from datetime import datetime
from typing import List
from uuid import UUID

@dataclasses(frozenset=True)
class UserQuery:
    prompt: str
    temperature: float
    stop_words: List[str]

@dataclasses(frozenset=True)
class LLMQuery:
    id: UUID
    ip_address: str
    raw_text: str
    create_at: datetime
