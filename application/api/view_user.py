from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.models.db_helper import db_helper
from application.core.models.user import PositionType, User
from application.core.schemas.user import SUserCreate, SUser
from application.crud.users import create_user, get_my_profile
from application.utils.dependencies import get_current_user

router = APIRouter(
    tags=["User"],
    prefix="/user"
)


@router.get("/my_profile")
async def get_profile(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ],
        current_user: User = Depends(get_current_user)
) -> SUser:
    profile = await get_my_profile(current_user.id, session)
    return profile
