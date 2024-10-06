from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse

from application.core.models.db_helper import db_helper
from application.core.models.user import User
from application.core.schemas.user import SUser
from application.crud.users import get_my_profile, get_users
from application.pages.router_admin import templates_admin
from application.pages.router_base import templates
from application.utils.dependencies import get_current_user

router = APIRouter(tags=["User"], prefix="/user")


@router.get("/my_profile")
async def get_profile(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: User = Depends(get_current_user),
) -> SUser:
    profile = await get_my_profile(current_user.id, session)
    profile.position = profile.position.value.title()
    return templates.TemplateResponse(
        "profile.html", {"request": request, "profile": profile}
    )


@router.get("/all")
async def get_all_users(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    current_user: User = Depends(get_current_user),
):
    if current_user.is_director:
        users = await get_users(session)
        return templates_admin.TemplateResponse("view_user_admin.html", {"request": request, "users": users})
    else:
        return {"message": "У вас нет прав для доступа"}
