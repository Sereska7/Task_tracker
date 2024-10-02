from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.models import User
from application.core.models.user import PositionType
from application.core.schemas.user import SUserCreate, SUser
from application.utils.auth_user import get_password_hash


async def create_user(
        position: PositionType,
        user_data: SUserCreate,
        session: AsyncSession
) -> SUser:
    hash_password = get_password_hash(user_data.password)
    user = User(
        name=user_data.name,
        email=user_data.email,
        hash_password=hash_password,
        position=position,
    )
    session.add(user)
    await session.commit()
    return user


async def get_user(
        session: AsyncSession,
        **data: dict
):
    stmt = select(User.__table__.columns).filter_by(**data)
    user = await session.execute(stmt)
    return user.mappings().one_or_none()


async def get_my_profile(
        user_id: int,
        session: AsyncSession
):
    stmt = select(User).where(User.id == user_id)
    user = await session.execute(stmt)
    return user.scalar()
