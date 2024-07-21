from pydantic import BaseModel


class GetChatQuery(BaseModel):
    id: str
