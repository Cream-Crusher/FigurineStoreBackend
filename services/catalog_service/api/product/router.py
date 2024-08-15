from typing import List

from fastapi import APIRouter

from api.product.schema import ProductRead, ProductCreate, ProductUpdate
from api.product.service import product_service

router = APIRouter(prefix='/product', tags=['Product|Products'])


@router.get('/', name='Get All Product', response_model=List[ProductRead])
async def get_all_products(products=product_service):
    return await products.all()


@router.get('/{product_id}', name='Get Product By Id', response_model=ProductRead)
async def product_by_id(product_id: str, products=product_service):
    return await products.id(product_id)


@router.post('/', name='Create Product', status_code=201)
async def create_product(product: ProductCreate, products=product_service):
    return await products.create(product.__dict__)


@router.delete('/{product_id}', name='Delete Product By Id')
async def del_product(product_id: str, products=product_service):
    return await products.delete(product_id)


@router.patch('/', name='Update Product By Id', response_model=ProductRead)
async def update_product(product_id: str, product: ProductUpdate, products=product_service):
    return await products.update(product_id, product.__dict__)
