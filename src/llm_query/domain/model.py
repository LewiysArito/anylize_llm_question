import dataclasses
from datetime import datetime
from typing import List
from uuid import UUID
from __future__ import annotations
from typing import List

@dataclasses(frozenset=True)
class UserQuery:
    prompt: str
    temperature: float
    model: str

@dataclasses(frozenset=True)
class UserQueryAnalysisRequest:
    id: UUID
    model: str
    ip_address: str
    raw_text: str
    create_at: datetime

