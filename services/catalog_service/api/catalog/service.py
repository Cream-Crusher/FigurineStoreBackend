from fastapi import Depends

from api.catalog.model import Product
from utils.base.service import BaseRepository
from utils.base.session import AsyncDatabase


class ProductService(BaseRepository):
    model = Product


async def get_product_service(session=Depends(AsyncDatabase.get_client)):
    return ProductService(session)


product_service: ProductService = Depends(get_product_service)
