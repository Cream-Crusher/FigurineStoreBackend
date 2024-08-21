from fastapi import APIRouter, HTTPException

from services.basket_service.api.basket.schema import AddItem, DelItem, BasketRead
from services.basket_service.api.basket.service import basket_service

router = APIRouter(prefix='/basket', tags=['Baskets|basket'])


@router.get('/get_basket_by_user_id', name='Add item for basket', response_model=BasketRead, status_code=201)
async def add_item(user_id: str, baskets=basket_service):
    return await baskets.get(user_id)


@router.post('/add_item', name='Add item for basket', status_code=201)
async def add_item(item: AddItem, baskets=basket_service):
    return await baskets.add_item(item.user_id, item.item_id, item.quantity)


@router.post('/del_item', name='Del item for basket', status_code=201)
async def del_item(item: DelItem, baskets=basket_service):
    return await baskets.del_item(item.user_id, item.item_id, item.quantity)


@router.post('/del_item', name='Del item for basket', status_code=201)
async def del_item(item: DelItem, baskets=basket_service):
    return await baskets.del_item(item.user_id, item.item_id, item.quantity)
