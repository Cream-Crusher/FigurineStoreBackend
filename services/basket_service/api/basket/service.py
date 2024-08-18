from fastapi import Depends, HTTPException

from services.basket_service.utils.cache.redis import RedisRepository
from services.basket_service.api.basket.model import Basket


class BasketService(RedisRepository):
    model = Basket

    async def create_busket(self, user_id):
        busket = self.model(user_id=user_id)
        await self.create(user_id, busket)

    async def update_item(self, user_id: str, item: str) -> 201:
        if not self.redis.exists(user_id):
            await self.create_busket(user_id)

        basket = await self.get(user_id)
        # self.model(basket)
        # if basket.items:


        return 201


async def get_basket_service():
    return BasketService()


basket_service: BasketService = Depends(get_basket_service)
