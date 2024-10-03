from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.models import User
from application.core.models.db_helper import db_helper
from application.core.schemas.project import SProject
from application.crud.projects import add_project, get_project, update_project, get_all_projects, del_project
from application.utils.dependencies import get_current_user

router = APIRouter(
    tags=["Project"],
    prefix="/project"
)


@router.post("/create")
async def create_project(
        data_project: SProject,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ],
        current_user: User = Depends(get_current_user)
) -> SProject | dict:
    if current_user.is_director:
        project = await add_project(data_project, session)
        return project
    else:
        return {"message": "У пользователя нет прав доступа"}


@router.patch("/update_{name}")
async def change_project(
        product_id: id,
        date_update: SProject,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ],
        current_user: User = Depends(get_current_user)
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
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ],
        current_user: User = Depends(get_current_user)
) -> List[SProject] | dict:
    projects = await get_all_projects(session)
    return projects


@router.delete("/delete")
async def delete_project(
        project_id: int,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ],
        current_user: User = Depends(get_current_user)
) -> dict:
    if current_user.is_director:
        return {"message": "У пользователя нет прав доступа"}
    project = await get_project(session, id=project_id)
    if not project:
        return {"message": "Нет такого проекта"}
    else:
        await del_project(project_id, session)
        return {"message": "successful"}
