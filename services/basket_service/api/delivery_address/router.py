from fastapi import APIRouter, HTTPException

from services.basket_service.api.delivery_address.schema import DeliveryAddressCreate, DeliveryAddressRead, \
    DeliveryAddressUpdate
from services.basket_service.api.delivery_address.service import delivery_address

router = APIRouter(prefix='/delivery_address', tags=['DeliveryAddress|Address'])


@router.get('/get_delivery_address/{user_id}', name='Get delivery address', response_model=DeliveryAddressRead, status_code=200)
async def get_delivery_address(user_id: str, address=delivery_address):
    return await address.get(user_id)


@router.post('/create_delivery_address', name='Add delivery address', status_code=201)
async def create_delivery_address(delivery_address: DeliveryAddressCreate, address=delivery_address):
    return await address.create(delivery_address.user_id, delivery_address)


@router.post('/update_delivery_address', name='update delivery address', status_code=201)
async def update_delivery_address(delivery_address: DeliveryAddressCreate, address=delivery_address):
    return await address.update_delivery_address(delivery_address.user_id, delivery_address)
