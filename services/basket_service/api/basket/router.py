from fastapi import APIRouter, HTTPException

from services.basket_service.api.basket.schema import UpdateItem
from services.basket_service.api.basket.service import basket_service

router = APIRouter(prefix='/basket', tags=['Baskets|basket'])


@router.post('/add_item', name='Add item for basket', status_code=201)
async def add_item(item: UpdateItem, baskets=basket_service):
    return await baskets.update_item(item.user_id, item.item_id)


@router.post('/del_item', name='Del item for basket', status_code=201)
async def add_item(item: UpdateItem, baskets=basket_service):
    return await baskets.del_item(item.user_id, item.item_id)
