import uuid
from datetime import datetime


class BaseEntity:

    def __init__(self):
        self.id: uuid.UUID
        self.created_at: datetime
        self.updated_at: datetime
