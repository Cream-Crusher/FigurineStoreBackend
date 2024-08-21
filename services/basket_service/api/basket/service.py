from fastapi import Depends, HTTPException

from services.basket_service.utils.cache.redis import RedisRepository
from services.basket_service.api.basket.model import Basket, BasketItem


class BasketService(RedisRepository):
    model = Basket

    @staticmethod
    async def get_user_item_by_item_id(basket: model, item_id: str) -> object | None:
        item = next(
            (item for item in basket.items if item.item_id == item_id),
            None
        )

        return item

    async def create_busket(self, user_id) -> 201:
        busket = self.model(user_id=user_id)
        await self.create(user_id, busket)

    async def add_item(self, user_id: str, item_id: str, quantity: int) -> 201:
        if not self.redis.exists(user_id):
            await self.create_busket(user_id)

        basket = await self.get(user_id)
        item = await self.get_user_item_by_item_id(basket, item_id)

        if item is None:
            item = BasketItem(item_id=item_id, quantity=0)
            basket.items.append(item)

        item.quantity += quantity

        await self.create(user_id, basket)

        return 201

    async def del_item(self, user_id: str, item_id: str, quantity: int) -> 201:
        basket = await self.get(user_id)
        item = await self.get_user_item_by_item_id(basket, item_id)

        if not item:
            raise HTTPException(status_code=400, detail="Item not found")

        item.quantity -= quantity

        if item.quantity <= 0:
            basket.items.remove(item)

        await self.create(user_id, basket)

        return 201


async def get_basket_service():
    return BasketService()


basket_service: BasketService = Depends(get_basket_service)
