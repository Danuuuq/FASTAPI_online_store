from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.database import Base, str_50, str_255, num_10_2


class Product(Base):
    sku: Mapped[str_50]
    name: Mapped[str_255]
    description: Mapped[str]
    price: Mapped[num_10_2]
    is_active: Mapped[bool]
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'),
                                             nullable=False)
    category: Mapped['Category'] = relationship(back_populates='products')


class Category(Base):
    name: Mapped[str_255] = mapped_column(index=True)  # добавлен индекс для поиска
    slug: Mapped[str_255] = mapped_column(unique=True)  # slug должен быть уникальным
    description: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=False)  # значение по умолчанию
    parent_category_id: Mapped[int] = mapped_column(ForeignKey('category.id'),
                                                    nullable=True,
                                                    index=True  # индекс для часто используемого внешнего ключа
                                                    )
    parent_category: Mapped['Category'] = relationship(
        remote_side='Category.id',
        back_populates='subcategories',
        lazy="joined"  # или "selectin" для оптимизации запросов
    )
    subcategories: Mapped[list['Category']] = relationship(back_populates='parent_category')
    products: Mapped[list['Product']] = relationship(back_populates='category')
