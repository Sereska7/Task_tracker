from sqlalchemy.ext.asyncio import AsyncSession

from application.core.models import Task
from application.core.models.task import TypeTask
from application.core.schemas.task import STask, ReadTask


async def add_task(
        data_task: STask,
        type_task: TypeTask,
        session: AsyncSession
) -> ReadTask:
    task = Task(type_task=type_task, **data_task.model_dump())
    session.add(task)
    await session.commit()
    return task
