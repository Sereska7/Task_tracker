from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from application.api.view_auth import router as router_auth
from application.api.view_user import router as router_user
from application.api.view_project import router as router_project
from application.api.view_tasks import router as router_task
from application.core.models.db_helper import db_helper
from application.pages.router_base import router as router_pages
from application.pages.router_admin import router as router_admin


# Определение асинхронного контекста жизненного цикла приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управление жизненным циклом приложения:
    - Запускает базу данных на старте.
    - Освобождает ресурсы и закрывает соединение с базой данных при завершении работы приложения.
    """
    # Действия при запуске приложения (startup)
    yield  # Приложение работает в это время
    # Действия при завершении работы приложения (shutdown)
    print("dispose engine")
    await db_helper.dispose()  # Закрытие соединения с базой данных


# Инициализация FastAPI-приложения с управлением жизненным циклом
main_app = FastAPI(lifespan=lifespan)

# Подключение всех маршрутов (роутеров) к приложению
main_app.include_router(router_auth)     # Роуты для авторизации
main_app.include_router(router_user)     # Роуты для пользователей
main_app.include_router(router_project)  # Роуты для проектов
main_app.include_router(router_task)     # Роуты для задач
main_app.include_router(router_pages)    # Роуты для страниц
main_app.include_router(router_admin)    # Роуты для административной панели

# Запуск приложения с авто-перезагрузкой при изменении кода
if __name__ == "__main__":
    uvicorn.run("application.main:main_app", reload=True)
