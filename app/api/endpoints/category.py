from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session, commit_change
from app.crud.category import category_crud
from app.schemas.category import CategoryCreate, CategoryDB, CategoryUpdate

router = APIRouter()


@router.post('/')
async def create_category(
    products: CategoryCreate | list[CategoryCreate],
    session: AsyncSession = Depends(get_async_session)
) -> None:
    if isinstance(products, list):
        await category_crud.bulk_create(products, session)
        return await commit_change(session)
    else:
        new_product = await category_crud.create(products, session)
        return await commit_change(session, new_product)
