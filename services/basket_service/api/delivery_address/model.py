from pydantic import BaseModel


class DeliveryAddress(BaseModel):
    user_id: str

    address_line: str
    country: str
    zip_code: str

    class Config:
        from_attributes = True
