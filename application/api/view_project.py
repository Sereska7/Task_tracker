from typing import Annotated, List

from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.models import User
from application.core.models.db_helper import db_helper
from application.core.schemas.project import SProject, SProjectCreateForm
from application.crud.projects import (
    add_project,
    get_project,
    update_project,
    get_all_projects,
    del_project,
)
from application.pages.router_base import templates
from application.pages.router_admin import templates_admin as templates_admit
from application.utils.dependencies import get_current_user

router = APIRouter(tags=["Project"], prefix="/project")


@router.post("/create")
async def create_project(
    request: Request,
    data_project: Annotated[SProjectCreateForm, Depends(SProjectCreateForm.as_form)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: User = Depends(get_current_user),
):
    if current_user.is_director:
        project = await add_project(data_project, session)
        projects = await get_all_projects(session)
        return templates_admit.TemplateResponse(
            "project_admin.html", {"request": request, "projects": projects, "message": "Проект успешно создан."}
        )
    else:
        return {"message": "У пользователя нет прав доступа"}


@router.patch("/update_{name}")
async def change_project(
    product_id: int,
    date_update: SProject,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: User = Depends(get_current_user),
) -> SProject | dict:
    if current_user.is_director:
        project = await get_project(session, id=product_id)
        if not project:
            return {"message": "Такого проекта не существует"}
        else:
            up_project = await update_project(project.name, session, date_update)
            return up_project
    else:
        return {"message": "У пользователя нет прав доступа"}


@router.get("/get")
async def get_projects(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: User = Depends(get_current_user),
) -> List[SProject] | dict:
    projects = await get_all_projects(session)
    if current_user.is_director:
        return templates_admit.TemplateResponse(
            "project_admin.html", {"request": request, "projects": projects}
        )
    else:
        return templates.TemplateResponse(
            "project.html", {"request": request, "projects": projects}
        )


@router.post("/delete")
async def delete_project(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: User = Depends(get_current_user),
    project_id: int = Form(...),
) -> dict:
    if current_user.is_director:
        project = await del_project(project_id, session)
        projects = await get_all_projects(session)
        return templates_admit.TemplateResponse(
            "project_admin.html",
            {
                "request": request,
                "projects": projects,
                "message": "Проект успешно удален",
            },
        )
    else:
        return {"message": "У пользователя нет прав доступа"}
