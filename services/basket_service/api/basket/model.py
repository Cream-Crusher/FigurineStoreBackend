from typing import List, Optional

from pydantic import BaseModel


class BasketItem(BaseModel):
    item_id: str
    quantity: int

    class Config:
        from_attributes = True


class Basket(BaseModel):
    user_id: str
    items: List[BasketItem]

    total_price: Optional[float]
    address_line: Optional[str]
    country: Optional[str]
    zip_code: Optional[str]

    class Config:
        from_attributes = True
