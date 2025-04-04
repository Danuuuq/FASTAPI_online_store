from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import commit_change


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_all(
        self,
        session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
    ):
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        return db_obj

    async def bulk_create(
        self,
        objs_in,
        session: AsyncSession
    ) -> None:
        for obj_in in objs_in:
            await self.create(obj_in, session)

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ):
        update_data = obj_in.dict(exclude_unset=True)
        obj_data = jsonable_encoder(db_obj)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        return commit_change(session, db_obj)

    async def filter_by_string(
        self,
        attr_name: str,
        attr_value: str,
        session: AsyncSession
    ):
        attr = getattr(self.model, attr_name)
        db_objs = await session.execute(
            select(self.model).filter(attr.ilike(f'%{attr_value}%'))
        )
        return db_objs.scalars().all()
