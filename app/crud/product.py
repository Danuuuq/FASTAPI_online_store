from decimal import Decimal

from sqlalchemy import select
from typing import Optional

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.products import Product, Category


class CRUDProduct(CRUDBase):

    async def get_category_products(
        self,
        category_slug: str,
        session: AsyncSession
    ):
        objects = await session.execute(
            select(self.model).join(self.model.category).where(
                Category.slug == category_slug
            )
        )
        return objects.scalars().all()

    async def filter_by_price(
        self,
        session: AsyncSession,
        min_price: Decimal = Decimal(0),
        max_price: Decimal | None = Decimal('Infinity')
    ):
        filter_objects = await session.execute(
            select(self.model).where(
                self.model.price >= min_price,
                self.model.price <= max_price
            )
        )
        return filter_objects.scalars().all()

    async def filter_products(
        self,
        session: AsyncSession,
        category_slug: str | None = None,
        min_price: Decimal | None = Decimal(0),
        max_price: Decimal | None = Decimal('Infinity'),
        **additional_filters
    ):
        query = select(self.model)
        if category_slug:
            query = query.join(self.model.category).where(
                Category.slug == category_slug
            )
        query = query.where(
            and_(self.model.price >= min_price,
                 self.model.price <= max_price)
            )
        for attr_name, attr_value in additional_filters.items():
            attr = getattr(self.model, attr_name, None)
            if attr:
                query = query.where(attr == attr_value)
        result = await session.execute(query)
        return result.scalars().all()


product_crud = CRUDProduct(Product)
