import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BaseEntity:
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
