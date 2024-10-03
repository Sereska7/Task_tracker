from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.models import User
from application.core.models.db_helper import db_helper
from application.core.models.task import TypeTask, TaskStatus
from application.core.schemas.task import STask, ReadTask
from application.crud.tasks import add_task, get_all_tasks, get_task, change_status_task
from application.utils.dependencies import get_current_user

router = APIRouter(
    tags=["Task"],
    prefix="/task"
)


@router.post("/create")
async def create_task(
        type_task: TypeTask,
        data_task: STask,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ],
        current_user: User = Depends(get_current_user)
):
    if current_user.is_director:
        task = await add_task(data_task, type_task, session)
        return task
    else:
        return {"message": "У пользователя нет прав доступа"}


@router.get("/get_all")
async def get_tasks(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ],
        current_user: User = Depends(get_current_user)
):
    return await get_all_tasks(session)


@router.get("/my")
async def get_my_tasks(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ],
        current_user: User = Depends(get_current_user)
):
    task = await get_task(session, contractor=current_user.id)
    return task


@router.patch("/accepted_for_work")
async def accepted_task(
        task_id: int,
        task_status: TaskStatus,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ],
        current_user: User = Depends(get_current_user)
):
    task = await get_task(session, id=task_id)
    if task.contractor == current_user.id:
        up_task = await change_status_task(
            task_id,
            current_user.id,
            session,
            status=task_status
        )
        return up_task
