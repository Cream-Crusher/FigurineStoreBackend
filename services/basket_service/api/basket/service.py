from fastapi import Depends, HTTPException

from services.basket_service.utils.cache.redis import RedisRepository
from services.basket_service.api.basket.model import Basket, BasketItem


class BasketService(RedisRepository):
    model = Basket

    async def create_busket(self, user_id):
        busket = await self.model(user_id=user_id)
        await self.create(user_id, busket)

    async def update_item(self, user_id: str, item_id: str) -> 201:
        if not self.redis.exists(user_id):
            await self.create_busket(user_id)

        basket = await self.get(user_id)

        item = next(
            (item for item in basket.items if item.item_id == item_id),
            BasketItem(item_id=user_id, quantity=0)
        )
        item.quantity += 1

        await self.create(user_id, basket)

        return 201


async def get_basket_service():
    return BasketService()


basket_service: BasketService = Depends(get_basket_service)
