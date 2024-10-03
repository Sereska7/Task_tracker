from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.models import User
from application.core.models.db_helper import db_helper
from application.core.models.task import TypeTask
from application.core.schemas.task import STask, ReadTask
from application.crud.tasks import add_task
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
) -> ReadTask:
    if current_user.is_director:
        task = await add_task(data_task, type_task, session)
        return task
    else:
        return {"message": "У пользователя нет прав доступа"}

