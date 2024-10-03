from sqlalchemy.ext.asyncio import AsyncSession

from application.core.models import Task
from application.core.schemas.task import STask, ReadTask


async def add_task(
        data_task: STask,
        session: AsyncSession
) -> ReadTask:
    task = Task(**data_task.model_dump())
    session.add(task)
    await session.commit()
    return task
