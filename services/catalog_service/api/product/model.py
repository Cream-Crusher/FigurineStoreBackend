from beanie import Document


class Product(Document):
    title: str
    price: str
    description: str
    size: str
    image_file: str
