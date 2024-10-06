from typing import Annotated

from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates

from application.core.models import User
from application.core.models.db_helper import db_helper
from application.core.models.task import TaskStatus, TypeTask
from application.crud.projects import get_all_projects
from application.crud.users import get_users
from application.utils.dependencies import get_current_user

# Роутер для страниц администратора
router = APIRouter(tags=["Admin"], prefix="/admin")

# Шаблоны для административных страниц
templates_admin = Jinja2Templates(directory="application/template/admin")


# Страница создания новой задачи
@router.get("/create_task")
async def create_task_page(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],  # Зависимость для получения сессии БД
    current_user: User = Depends(get_current_user),  # Получение текущего пользователя
):
    """
    Отображение страницы создания задачи.
    Доступно только для директора.
    """
    if current_user.is_director:
        # Получаем список всех проектов и пользователей для формы
        projects = await get_all_projects(session)
        users = await get_users(session)

        # Формируем списки для выпадающих списков с типами задач и статусами
        task_status_options = [(status.name, status.value) for status in TaskStatus]
        type_task_options = [(task.name, task.value) for task in TypeTask]

        # Возвращаем страницу с формой создания задачи
        return templates_admin.TemplateResponse(
            "create_task_admin.html",
            {
                "request": request,
                "projects": projects,
                "users": users,
                "task_status_options": task_status_options,
                "type_task_options": type_task_options,
            },
        )
    else:
        # Если пользователь не директор, отображаем сообщение об ошибке
        return templates_admin.TemplateResponse(
            "create_task_admin.html",
            {"request": request, "message": "У вас нет прав для создания задач"},
        )


# Страница создания нового проекта
@router.get("/create_project")
async def create_project_page(
    request: Request,
):
    """
    Отображение страницы создания проекта.
    """
    return templates_admin.TemplateResponse(
        "create_project_admin.html", {"request": request}
    )
