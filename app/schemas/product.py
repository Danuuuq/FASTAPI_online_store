from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from app.core.config import settings


class ProductBase(BaseModel):
    sku: Optional[str] = Field(max_length=settings.MAX_LENGTH_INFO)
    name: Optional[str] = Field(max_length=settings.MAX_LENGTH_NAME)
    description: Optional[str] = Field()
    price: Optional[Decimal] = Field(gt=settings.MIN_DECIMAL_PRICE,
                                     max_digits=settings.MAX_DECIMAL_PRICE)
    is_active: Optional[bool] = Field()

    class Config:
        extra = 'forbid'
        str_min_length = settings.MIN_LENGTH_NAME


class ProductCreate(ProductBase):
    sku: str = Field(max_length=settings.MAX_LENGTH_INFO)
    name: str = Field(max_length=settings.MAX_LENGTH_NAME)
    description: str = Field()
    price: Decimal = Field(max_digits=settings.MAX_DECIMAL_PRICE)
    is_active: bool = Field(default=False)


class ProductUpdate(ProductBase):
    pass


class ProductDB(ProductCreate):
    category_id: int

    class Config:
        from_attributes = True
