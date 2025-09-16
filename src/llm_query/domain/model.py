from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class UserQuery:
    prompt: str
    temperature: float
    model: str

@dataclass(frozen=True)
class UserQueryAnalysisRequest:
    id: UUID
    model: str
    ip_address: str
    raw_text: str
    create_at: datetime

