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

router = APIRouter(tags=["Admin"], prefix="/admin")

templates_admin = Jinja2Templates(directory="template/admin")


@router.get("/create_task")
async def create_task_page(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: User = Depends(get_current_user),
):
    if current_user.is_director:
        projects = await get_all_projects(session)
        users = await get_users(session)

        # Передаем перечисления TaskStatus и TypeTask как списки
        task_status_options = [(status.name, status.value) for status in TaskStatus]
        type_task_options = [(task.name, task.value) for task in TypeTask]

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
        return templates_admin.TemplateResponse(
            "create_task_admin.html",
            {"request": request, "message": "У вас нет прав для создания задач"},
        )


@router.get("/create_project")
async def create_project_page(
        request: Request,
):
    return templates_admin.TemplateResponse("create_project_admin.html", {"request": request})
