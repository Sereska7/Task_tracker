from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.models import Task, User, Project
from application.core.models.task import TypeTask
from application.core.schemas.task import (
    STask,
    SChangeTask,
    SMyTask,
    SBaseTask,
)


async def add_task(data_task: STask, type_task: TypeTask, session: AsyncSession):
    task = Task(type_task=type_task, **data_task.model_dump())
    session.add(task)
    await session.commit()
    return task


async def get_all_tasks(session: AsyncSession) -> SBaseTask:
    stmt = select(Task.__table__.columns)
    tasks = await session.execute(stmt)
    return tasks.mappings().all()


async def get_task(session: AsyncSession, **data: dict):
    stmt = select(Task.__table__.columns).filter_by(**data).order_by(Task.date_to)
    task = await session.execute(stmt)
    return task.mappings().one_or_none()


async def get_tasks_by_project(project_id: int, session: AsyncSession):
    stmt = select(Task.__table__.columns).where(Task.project_id == project_id)
    tasks = await session.execute(stmt)
    return tasks.mappings().all()


async def get_task_by_id(
    task_id: int,
    session: AsyncSession,
) -> SMyTask:
    stmt = (
        select(
            User.email.label("contractor_email"),
            Project.name.label("project_name"),
            Task.id,
            Task.name,
            Task.description,
            Task.date_from,
            Task.date_to,
            Task.status,
        )
        .join(User, Task.contractor == User.id)
        .join(Project, Task.project_id == Project.id)
        .where(Task.id == task_id)
        .order_by(Task.date_to)
    )
    result = await session.execute(stmt)
    return result.one_or_none()


async def get_my_tasks(
    user_id: int,
    session: AsyncSession,
) -> SMyTask:
    stmt = (
        select(
            User.email.label("contractor_email"),
            Project.name.label("project_name"),
            Task,
        )
        .join(User, Task.contractor == User.id)
        .join(Project, Task.project_id == Project.id)
        .where(Task.contractor == user_id)
        .order_by(Task.date_to)
    )
    result = await session.execute(stmt)
    tasks = [
        {
            **jsonable_encoder(task),
            "contractor_email": contractor_email,
            "project_name": project_name,
        }
        for contractor_email, project_name, task in result.all()
    ]
    return tasks


async def change_status_task(
    task_id: int, user_id: int, session: AsyncSession, **data: dict
):
    stmt = (
        update(Task)
        .filter_by(id=task_id, contractor=user_id)
        .values(**data)
        .returning(Task)
    )
    up_task = await session.execute(stmt)
    return up_task.scalar()


async def update_task(task_id: int, data_task: SChangeTask, session: AsyncSession):
    stmt = (
        update(Task)
        .filter_by(id=task_id)
        .values(data_task.model_dump())
        .returning(Task)
    )
    up_task = await session.execute(stmt)
    return up_task.scalar()


async def remove_task(task_id: int, session: AsyncSession):
    stmt = delete(Task).where(Task.id == task_id)
    await session.execute(stmt)
