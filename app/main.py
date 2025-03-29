import uvicorn
from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings

app = FastAPI(title=settings.APP_TITLE,
              description=settings.APP_DESCRIPTION)

app.include_router(main_router)


def main():
    uvicorn.run("main:app", host=settings.APP_HOST,
                port=settings.APP_PORT, reload=settings.RELOAD)


if __name__ == '__main__':
    main()
