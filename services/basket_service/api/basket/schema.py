from typing import Optional

from pydantic import BaseModel, Field


class BasketItem(BaseModel):
    item_id: str
    quantity: int


class BasketRead(BaseModel):
    user_id: str
    items: Optional[list]
    total_price: Optional[float] = 0


class UpdateDeliveryAddress(BaseModel):
    address_line: str
    country: str
    zip_code: str


class AddItem(BaseModel):
    user_id: str
    item_id: str
    quantity: int = Field(ge=1, lt=99)


class DelItem(BaseModel):
    user_id: str
    item_id: str
    quantity: int = Field(ge=1, lt=99)
