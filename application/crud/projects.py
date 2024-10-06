from enum import Enum

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.models import Project
from application.core.schemas.project import SProject


# Добавление нового проекта в базу данных
async def add_project(data: SProject, session: AsyncSession) -> SProject:
    """
    Создает новый проект в базе данных на основе переданных данных.

    :param data: Схема SProject с данными для нового проекта.
    :param session: Асинхронная сессия базы данных.
    :return: Возвращает созданный объект проекта.
    """
    # Преобразуем данные схемы в модель
    project = Project(**data.model_dump())

    # Добавляем в сессию и коммитим
    session.add(project)
    await session.commit()

    return project


# Получение одного проекта по фильтрам
async def get_project(session: AsyncSession, **data: dict):
    """
    Возвращает один проект по переданным фильтрам (например, по id или имени).

    :param session: Асинхронная сессия базы данных.
    :param data: Словарь с фильтрами для поиска проекта (например, {'name': 'project_name'}).
    :return: Возвращает найденный проект или None, если проект не найден.
    """
    stmt = select(Project).filter_by(**data)
    project = await session.execute(stmt)

    return project.one_or_none()


# Получение всех проектов
async def get_all_projects(session: AsyncSession):
    """
    Возвращает список всех проектов в базе данных.

    :param session: Асинхронная сессия базы данных.
    :return: Список всех проектов в виде отображений (mappings).
    """
    stmt = select(Project.__table__.columns)
    projects = await session.execute(stmt)

    # Возвращаем все проекты в виде списка отображений
    return projects.mappings().all()


# Обновление проекта
async def update_project(
    name_project: str, session: AsyncSession, date_update: SProject
):
    """
    Обновляет проект по его имени.

    :param name_project: Имя проекта, который нужно обновить.
    :param session: Асинхронная сессия базы данных.
    :param date_update: Схема SProject с обновленными данными.
    :return: Возвращает обновленный проект.
    """
    stmt = (
        update(Project)
        .filter_by(name=name_project)
        .values(name=date_update.name, description=date_update.description)
        .returning(Project)
    )

    # Выполняем обновление и коммитим
    up_project = await session.execute(stmt)
    await session.commit()

    return up_project.scalar_one_or_none()


# Удаление проекта по id
async def del_project(project_id: int, session: AsyncSession):
    """
    Удаляет проект по его идентификатору (id).

    :param project_id: ID проекта, который нужно удалить.
    :param session: Асинхронная сессия базы данных.
    :return: Словарь с сообщением об успешном удалении.
    """
    stmt = delete(Project).where(Project.id == project_id)

    # Выполняем удаление и коммитим
    await session.execute(stmt)
    await session.commit()

    return {"message": "Проект успешно удален"}
