from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.models import Task
from application.core.models.task import TypeTask
from application.core.schemas.task import STask, ReadTask


async def add_task(
        data_task: STask,
        type_task: TypeTask,
        session: AsyncSession
):
    task = Task(type_task=type_task, **data_task.model_dump())
    session.add(task)
    await session.commit()
    return task


async def get_all_tasks(
        session: AsyncSession
):
    stmt = select(Task.__table__.columns)
    tasks = await session.execute(stmt)
    return tasks.mappings().all()


async def get_task(
        session: AsyncSession,
        **data: dict
):
    stmt = (select(Task.__table__.columns)
            .filter_by(**data)
            .order_by(Task.date_to))
    task = await session.execute(stmt)
    return task.mappings().one_or_none()


async def change_status_task(
        task_id: int,
        user_id: int,
        session: AsyncSession,
        **data: dict
):
    stmt = (
        update(Task)
        .filter_by(
            id=task_id,
            contractor=user_id
        )
        .values(**data)
        .returning(Task)
    )
    up_task = await session.execute(stmt)
    return up_task.scalar()
