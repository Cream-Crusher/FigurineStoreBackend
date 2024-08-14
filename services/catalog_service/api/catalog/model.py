from enum import Enum

from beanie import Document


class Size(str, Enum):
    large = "Large"
    medium = "Medium"
    small = "Small"


class Product(Document):
    title: str
    price: str
    description: str
    size: Size
