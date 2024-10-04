from enum import Enum

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.models import Project
from application.core.schemas.project import SProject


async def add_project(data: SProject, session: AsyncSession) -> SProject:
    project = Project(**data.model_dump())
    session.add(project)
    await session.commit()
    return project


async def get_project(session: AsyncSession, **data: dict):
    stmt = select(Project).filter_by(**data)
    project = await session.execute(stmt)
    return project.one_or_none()


async def get_all_projects(session: AsyncSession):
    stmt = select(Project.__table__.columns)
    projects = await session.execute(stmt)
    return projects.mappings().all()


async def update_project(
    name_project: str, session: AsyncSession, date_update: SProject
):
    stmt = (
        update(Project)
        .filter_by(name=name_project)
        .values(name=date_update.name, description=date_update.description)
        .returning(Project)
    )
    up_project = await session.execute(stmt)
    await session.commit()
    return up_project.scalar_one_or_none()


async def del_project(project_id: int, session: AsyncSession):
    stmt = delete(Project).where(Project.id == project_id)
    await session.execute(stmt)
    await session.commit()
    return {"message": "successful"}
