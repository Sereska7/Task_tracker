from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.models import Task, User, Project
from application.core.schemas.task import (
    SChangeTask,
    SMyTask,
    SBaseTask,
)


# Функция для добавления новой задачи
async def add_task(data_task: SBaseTask, session: AsyncSession) -> Task:
    """
    Добавляет новую задачу в базу данных.

    :param data_task: Схема SBaseTask с данными задачи.
    :param session: Асинхронная сессия базы данных.
    :return: Возвращает созданную задачу.
    """
    task = Task(**data_task.model_dump())
    session.add(task)
    await session.commit()
    return task


# Получение всех задач
async def get_all_tasks(session: AsyncSession) -> list:
    """
    Возвращает все задачи.

    :param session: Асинхронная сессия базы данных.
    :return: Список задач в виде отображений (mappings).
    """
    stmt = select(Task.__table__.columns)
    tasks = await session.execute(stmt)
    return tasks.mappings().all()


# Получение задачи по фильтрам
async def get_task(session: AsyncSession, **data: dict) -> Task:
    """
    Возвращает одну задачу по фильтрам (например, по id или другим параметрам).

    :param session: Асинхронная сессия базы данных.
    :param data: Фильтры для поиска задачи.
    :return: Найденная задача или None.
    """
    stmt = select(Task.__table__.columns).filter_by(**data).order_by(Task.date_to)
    task = await session.execute(stmt)
    return task.mappings().one_or_none()


# Получение задач по проекту
async def get_tasks_by_project(project_id: int, session: AsyncSession) -> list:
    """
    Возвращает задачи по ID проекта.

    :param project_id: ID проекта.
    :param session: Асинхронная сессия базы данных.
    :return: Список задач проекта.
    """
    stmt = select(Task.__table__.columns).where(Task.project_id == project_id)
    tasks = await session.execute(stmt)
    return tasks.mappings().all()


# Получение задачи по ID
async def get_task_by_id(task_id: int, session: AsyncSession) -> dict:
    """
    Возвращает задачу по ее ID, включая информацию о проекте и исполнителе.

    :param task_id: ID задачи.
    :param session: Асинхронная сессия базы данных.
    :return: Словарь с данными задачи, проекта и исполнителя или None.
    """
    stmt = (
        select(
            User.email.label("contractor_email"),
            Project.name.label("project_name"),
            Task.id,
            Task.name,
            Task.description,
            Task.date_from,
            Task.date_to,
            Task.type_task,
            Task.status,
        )
        .join(User, Task.contractor == User.id)
        .join(Project, Task.project_id == Project.id)
        .where(Task.id == task_id)
        .order_by(Task.date_to)
    )
    result = await session.execute(stmt)
    return result.one_or_none()


# Получение задач пользователя
async def get_my_tasks(user_id: int, session: AsyncSession) -> list:
    """
    Возвращает все задачи, назначенные на пользователя.

    :param user_id: ID пользователя.
    :param session: Асинхронная сессия базы данных.
    :return: Список задач пользователя.
    """
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

    # Возвращаем список задач в виде словарей
    tasks = [
        {
            **jsonable_encoder(task),
            "contractor_email": contractor_email,
            "project_name": project_name,
        }
        for contractor_email, project_name, task in result.all()
    ]
    return tasks


# Изменение статуса задачи
async def change_status_task(
    task_id: int, user_id: int, session: AsyncSession, **data: dict
) -> Task:
    """
    Изменяет статус задачи для исполнителя.

    :param task_id: ID задачи.
    :param user_id: ID исполнителя (контрактора).
    :param session: Асинхронная сессия базы данных.
    :param data: Данные для обновления (статус задачи).
    :return: Обновленная задача.
    """
    stmt = (
        update(Task)
        .filter_by(id=task_id, contractor=user_id)
        .values(**data)
        .returning(Task)
    )
    up_task = await session.execute(stmt)
    await session.commit()
    return up_task.scalar()


# Обновление задачи
async def update_task(
    task_id: int, data_task: SChangeTask, session: AsyncSession
) -> Task:
    """
    Обновляет задачу по ее ID.

    :param task_id: ID задачи.
    :param data_task: Данные для обновления.
    :param session: Асинхронная сессия базы данных.
    :return: Обновленная задача.
    """
    stmt = (
        update(Task)
        .filter_by(id=task_id)
        .values(data_task.model_dump())
        .returning(Task)
    )
    up_task = await session.execute(stmt)
    await session.commit()
    return up_task.scalar()


# Удаление задачи
async def remove_task(task_id: int, session: AsyncSession):
    """
    Удаляет задачу по ее ID.

    :param task_id: ID задачи.
    :param session: Асинхронная сессия базы данных.
    """
    stmt = delete(Task).where(Task.id == task_id)
    await session.execute(stmt)
    await session.commit()
