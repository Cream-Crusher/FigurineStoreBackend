from pydantic import BaseModel


class UpdateUserData(BaseModel):
    fullname: str
    username: str
    phone: str
    email: str
