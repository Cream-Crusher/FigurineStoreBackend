from typing import List

from fastapi import APIRouter

from api.catalog.schema import ProductRead, ProductCreate
from api.catalog.service import product_service

router = APIRouter(prefix='/product', tags=['Product|Products'])


@router.get('/', name='Get All Product', response_model=List[ProductRead])
async def get_all_products(products=product_service):
    return await products.all()


@router.get('/{product_id}', name='Get Product By Id', response_model=ProductRead)
async def product_by_id(product_id: str, products=product_service):
    return await products.id(product_id)


@router.post('/', name='Create Product', status_code=201)
async def create_blog(product: ProductCreate, products=product_service):
    return await products.create(product.__dict__)

# @router.delete('/{blog_id}', name='Delete Blog By Id')
# async def del_blog(blog_id: str, blogs=blog_service, me=Depends(get_me)):
#     blog_owner_id = (await blogs.id(blog_id)).owner_id
#
#     if not (me.role in ["admin"] or blog_owner_id in me.roles):
#         raise HTTPException(403, "forbidden")
#
#     return await blogs.delete(blog_id)
#
#
# @router.patch('/', name='Update Blog By Id', response_model=BlogRead)
# async def update_blog(blog_id: str, blog: BlogUpdate, blogs=blog_service, me=Depends(get_me)):
#     blog_owner_id = (await blogs.id(blog_id)).owner_id
#
#     if not (me.role in ["admin"] or blog_owner_id in me.roles):
#         raise HTTPException(403, "forbidden")
#
#     return await blogs.update(blog_id, blog.__dict__)
