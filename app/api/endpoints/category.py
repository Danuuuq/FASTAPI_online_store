from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session, commit_change
from app.crud.category import category_crud
from app.schemas.category import CategoryCreate, CategoryDB, CategoryUpdate

router = APIRouter()


@router.get(
    '/',
    response_model=list[CategoryDB]
)
async def get_all_category(
    session: AsyncSession = Depends(get_async_session)
) -> list[CategoryDB]:
    return await category_crud.get_all(session)


@router.post('/')
async def create_category(
    category: CategoryCreate | list[CategoryCreate],
    session: AsyncSession = Depends(get_async_session)
) -> None:
    if isinstance(category, list):
        await category_crud.bulk_create(category, session)
        return await commit_change(session)
    else:
        new_category = await category_crud.create(category, session)
        return await commit_change(session, new_category)
