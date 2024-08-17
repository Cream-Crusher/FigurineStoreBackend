from fastapi import Depends

from services.catalog_service.api.product.model import Product
from services.catalog_service.utils.base.service import BaseRepository
from services.catalog_service.utils.base.session import AsyncDatabase


class ProductService(BaseRepository):
    model = Product


async def get_product_service(session=Depends(AsyncDatabase.get_client)):
    return ProductService(session)


product_service: ProductService = Depends(get_product_service)
