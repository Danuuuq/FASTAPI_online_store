from datetime import datetime
from decimal import Decimal
from typing import Annotated

from fastapi import HTTPException
from sqlalchemy import func, String, Numeric
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import (
    AsyncAttrs, AsyncSession, async_sessionmaker, create_async_engine
)
from sqlalchemy.orm import (
    DeclarativeBase, declared_attr, Mapped, mapped_column, registry
)

from app.core.config import settings

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Логирование SQL-запросов (удобно для разработки)
    echo_pool="debug",  # Добавьте это для логирования пула соединений
    pool_pre_ping=True,  # Проверка соединения перед использованием
    pool_size=20,  # Размер пула соединений
    max_overflow=10
)
async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,  # Не истекать после коммита (удобно для работы с объектами после сохранения)
    autoflush=False  # Автосброс лучше отключить для явного управления
)

int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(),
                                               onupdate=func.now())]
str_50 = Annotated[str, settings.MAX_LENGTH_INFO]
str_255 = Annotated[str, settings.MAX_LENGTH_NAME]
num_10_2 = Annotated[Decimal, settings.MAX_DECIMAL_PRICE]
str_unique = Annotated[str, mapped_column(unique=True, nullable=False)]
str_nullable = Annotated[str, mapped_column(nullable=True)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    registry = registry(
        type_annotation_map={
            str_50: String(settings.MAX_LENGTH_INFO),
            str_255: String(settings.MAX_LENGTH_NAME),
            num_10_2: Numeric(settings.MAX_DECIMAL_PRICE,
                              settings.PRECISION_PRICE)
        }
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


async def get_async_session():
    async with async_session_maker() as async_session:
        yield async_session


async def commit_change(session: AsyncSession, obj=None):
    """Безопасное выполнение сохранения в БД"""
    try:
        await session.commit()
        if obj:
            await session.refresh(obj)
    except IntegrityError as e:
        await session.rollback()
        # Логируем полную информацию об ошибке
        print(f"IntegrityError: {e.orig}")  # или используйте logging
        raise HTTPException(
            status_code=400,
            detail=f"Ошибка целостности данных: {str(e.orig)}"
        )
    except SQLAlchemyError as e:
        await session.rollback()
        print(f"SQLAlchemyError: {str(e)}")  # или используйте logging
        raise HTTPException(
            status_code=500,
            detail=f'Ошибка сохранения в БД: {str(e)}'
        )
    else:
        return obj
