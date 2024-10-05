from typing import Annotated, List, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.background_tasks.send_message import (
    send_email_add_new_task_for_you,
    send_email_change_task_for_you,
    send_email_accept_task,
)
from application.core.models import User
from application.core.models.db_helper import db_helper
from application.core.models.task import TypeTask, TaskStatus
from application.core.schemas.task import (
    STask,
    ReadTask,
    SChangeTask,
    SBaseTask,
    SMyTask,
)
from application.crud.tasks import (
    add_task,
    get_all_tasks,
    get_task,
    change_status_task,
    update_task,
    get_my_tasks,
    get_task_by_id,
    remove_task,
    get_tasks_by_project,
)
from application.utils.dependencies import get_current_user
from application.utils.detected import detect_changes

router = APIRouter(tags=["Task"], prefix="/task")


@router.post("/create")
async def create_task(
    type_task: TypeTask,
    data_task: STask,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: User = Depends(get_current_user),
):
    if current_user.is_director:
        new_task = await add_task(data_task, type_task, session)
        task = await get_task_by_id(new_task.id, session)
        send_email_add_new_task_for_you(task.contractor_email, task)
        return new_task
    else:
        return {"message": "У пользователя нет прав доступа"}


@router.get("/get_all")
async def get_tasks(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: User = Depends(get_current_user),
) -> List[SBaseTask]:
    return await get_all_tasks(session)


@router.get("/my_tasks")
async def view_my_tasks(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: User = Depends(get_current_user),
) -> List[SMyTask]:
    user_id = current_user.id
    task = await get_my_tasks(user_id, session)
    return task


@router.get("/get_task")
async def view_task(
    task_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: User = Depends(get_current_user),
) -> SMyTask:
    task = await get_task_by_id(task_id, session)
    return task


@router.get("/by_project")
async def view_task_by_project(
    project_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: User = Depends(get_current_user),
) -> List[SBaseTask]:
    tasks = await get_tasks_by_project(project_id, session)
    return tasks


@router.patch("/accepted_for_work")
async def accepted_task(
    task_id: int,
    task_status: TaskStatus,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: User = Depends(get_current_user),
):
    task = await get_task(session, id=task_id)
    if task.contractor == current_user.id:
        up_task = await change_status_task(
            task_id, current_user.id, session, status=task_status
        )
        task = await get_task_by_id(up_task.id, session)
        send_email_accept_task(task.contractor_email, task)
        return up_task


@router.patch("/change")
async def change_task(
    task_id: int,
    data_task: SChangeTask,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: User = Depends(get_current_user),
) -> SBaseTask | dict:
    if current_user.is_director:
        current_task = await get_task_by_id(task_id, session)
        changed_fields = detect_changes(current_task, data_task)
        up_task = await update_task(task_id, data_task, session)
        if changed_fields:
            send_email_change_task_for_you(
                current_task.contractor_email, changed_fields
            )
        return up_task
    else:
        return {"message": "У пользователя нет прав доступа"}


@router.delete("/delete")
async def del_task(
    task_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: User = Depends(get_current_user),
):
    if current_user.is_director:
        task = await get_task(session, id=task_id)
        if not task:
            return {"message": "Задача не найдена"}
        else:
            await remove_task(task_id, session)
            return {"message": "Задача удалена"}
    else:
        return {"message": "У пользователя нет прав доступа"}
