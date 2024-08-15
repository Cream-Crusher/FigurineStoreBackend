from enum import Enum

from beanie import PydanticObjectId

from pydantic import BaseModel, Field


class Size(str, Enum):
    large = "Large"
    medium = "Medium"
    small = "Small"


class Product(BaseModel):
    title: str = Field(max_length=100)
    price: str
    description: str = Field(default=None, max_length=1000)
    size: Size


class ProductRead(Product):
    id: PydanticObjectId = Field()


class ProductCreate(Product):
    pass


class ProductUpdate(Product):
    pass