from services.basket_service.utils.base.BaseServiceAPI import BaseServiceAPI
from services.basket_service.utils.base.config import settings


class CatalogAPI(BaseServiceAPI):

    def __init__(self):
        super().__init__(base_url=settings.base_service_url.catalog)

    async def get_product(self, product_id: str) -> dict:
        url = f"product/{product_id}"

        product = await self.get(url)
        return product


catalog_api = CatalogAPI()
