from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session, commit_change
from app.crud.product import product_crud
from app.schemas.product import ProductCreate, ProductDB, ProductUpdate

router = APIRouter()


@router.get('/', response_model=list[ProductDB])
async def get_all_products(session: AsyncSession = Depends(get_async_session)):
    return await product_crud.get_all(session)


@router.get('/{product_id}', response_model=ProductDB)
async def get_product(
    product_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    return await product_crud.get(product_id, session)


@router.get('/{category_slug}', response_model=list[ProductDB])
async def get_category_products(
    category_slug: str,
    session: AsyncSession = Depends(get_async_session)
):
    return await product_crud.get_category_products(category_slug, session)


@router.post('/', response_model=ProductCreate)
async def create_product(
    products: ProductCreate | list[ProductCreate],
    session: AsyncSession = Depends(get_async_session)
) -> ProductDB | None:
    if isinstance(products, list):
        await product_crud.bulk_create(products, session)
    else:
        new_product = await product_crud.create(products, session)
    return await commit_change(session, new_product)
