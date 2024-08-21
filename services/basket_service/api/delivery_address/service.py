from fastapi import Depends, HTTPException

from services.basket_service.api.delivery_address.model import DeliveryAddress
from services.basket_service.utils.cache.redis import RedisRepository


class DeliveryAddressService(RedisRepository):
    model = DeliveryAddress

    async def update_delivery_address(self, user_id: str, new_delivery_address: object):
        await self.update(user_id, new_delivery_address.__dict__)



async def get_delivery_address_service():
    return DeliveryAddressService()


delivery_address: DeliveryAddressService = Depends(get_delivery_address_service)
