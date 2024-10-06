from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.models.db_helper import db_helper
from application.core.models.user import User
from application.core.schemas.user import SUser
from application.crud.users import get_my_profile, get_users
from application.pages.router_admin import templates_admin
from application.pages.router_base import templates
from application.utils.dependencies import get_current_user

# Маршрутизатор для управления пользователями
router = APIRouter(tags=["User"], prefix="/user")


# Роутер для получения профиля текущего пользователя
@router.get("/my_profile")
async def get_profile(
    request: Request,  # Объект запроса
    session: Annotated[
        AsyncSession, Depends(db_helper.session_getter)
    ],  # Сессия базы данных
    current_user: User = Depends(
        get_current_user
    ),  # Текущий авторизованный пользователь
) -> SUser:
    """
    Получение профиля текущего пользователя:
    - Возвращает данные профиля и отображает страницу профиля.
    """
    profile = await get_my_profile(current_user.id, session)
    # Преобразуем позицию пользователя в читабельный формат
    profile.position = profile.position.value.title()

    # Возвращаем шаблон с профилем
    return templates.TemplateResponse(
        "profile.html", {"request": request, "profile": profile}
    )


# Роутер для получения списка всех пользователей
@router.get("/all")
async def get_all_users(
    request: Request,  # Объект запроса
    session: Annotated[
        AsyncSession, Depends(db_helper.session_getter)
    ],  # Сессия базы данных
    current_user: User = Depends(
        get_current_user
    ),  # Текущий авторизованный пользователь
):
    """
    Получение списка всех пользователей:
    - Доступно только для пользователей с правами директора.
    - Возвращает список всех пользователей на странице администратора.
    """
    if current_user.is_director:
        # Получаем всех пользователей
        users = await get_users(session)

        # Возвращаем админский шаблон с пользователями
        return templates_admin.TemplateResponse(
            "view_user_admin.html", {"request": request, "users": users}
        )
    else:
        # Если у пользователя нет прав директора, возвращаем сообщение об отказе в доступе
        return {"message": "У вас нет прав для доступа"}
