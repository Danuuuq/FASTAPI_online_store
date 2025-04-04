from typing import Optional

from pydantic import BaseModel, Field

from app.core.config import settings


class CategoryBase(BaseModel):
    name: Optional[str] = Field(max_length=settings.MAX_LENGTH_NAME)
    slug: Optional[str] = Field(max_length=settings.MAX_LENGTH_NAME)
    description: Optional[str] = Field()
    parent_category_id: Optional[int] = Field()
    child_category: Optional[list[int]] = Field()
    is_active: Optional[bool] = Field()

    class Config:
        extra = 'forbid'
        str_min_length = settings.MIN_LENGTH_NAME


class CategoryCreate(BaseModel):
    name: str = Field(max_length=settings.MAX_LENGTH_NAME)
    slug: str = Field(max_length=settings.MAX_LENGTH_NAME)
    description: str = Field()
    parent_category_id: int | None
    is_active: bool = Field()


class CategoryUpdate(CategoryBase):
    pass


class CategoryDB(CategoryCreate):
    # parent_category_id: int

    class Config:
        from_attributes = True
