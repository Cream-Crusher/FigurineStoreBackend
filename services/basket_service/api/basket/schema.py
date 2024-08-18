from pydantic import BaseModel


class BasketItem(BaseModel):
    item_id: str
    quantity: int


class BasketRead(BaseModel):
    user_id: str
    items: list
    total_price: float
    address_line: str
    country: str
    zip_code: str


class UpdateDeliveryAddress(BaseModel):
    address_line: str
    country: str
    zip_code: str


class UpdateItem(BaseModel):
    user_id: str
    item_id: str
