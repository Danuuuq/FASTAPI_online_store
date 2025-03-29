import os
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_TITLE: str = 'Онлайн магазин'
    APP_DESCRIPTION: str = 'Покупки онлайн доступны, как и всегда'
    APP_HOST: str = '127.0.0.1'
    APP_PORT: int = 8000
    RELOAD: bool = False
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = None
    DB_NAME: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    PRECISION_PRICE: int = 2
    MAX_DECIMAL_PRICE: int = 10
    MAX_LENGTH_NAME: int = 255
    MAX_LENGTH_INFO: int = 50
    MIN_DECIMAL_PRICE: int = 0
    MIN_LENGTH_NAME: int = 1
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              '..', '.env'),
        env_file_encoding='utf-8')

    def get_db_url(self):
        return (f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@'
                f'{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}')


settings = Settings()
