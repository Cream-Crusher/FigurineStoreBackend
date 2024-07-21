from pydantic import BaseModel


class GetChatResponse(BaseModel):
    id: str
    first_user_id: str
    second_user_id: str
