from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Event:
    id: UUID
    event_type: str
    content: dict
    created_at: datetime
    processed_at: datetime