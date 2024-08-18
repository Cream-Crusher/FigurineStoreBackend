from typing import List

from pydantic import BaseModel


class BasketItem(BaseModel):
    item_id: str
    quantity: int

    class Config:
        orm_mode = True


class Basket(BaseModel):
    user_id: str
    items: List[BasketItem] = []

    total_price: float = 0
    address_line: str = None
    country: str = None
    zip_code: str = None

    class Config:
        orm_mode = True
