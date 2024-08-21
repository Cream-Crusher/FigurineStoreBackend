from typing import List, Optional

from pydantic import BaseModel


class BasketItem(BaseModel):
    item_id: str
    quantity: int

    class Config:
        from_attributes = True


class Basket(BaseModel):
    user_id: str
    items: List[BasketItem] = []

    total_price: float = 0

    class Config:
        from_attributes = True
