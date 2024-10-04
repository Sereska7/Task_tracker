import json
from random import randint
from typing import Annotated, Dict

import asyncio
from fastapi import APIRouter, HTTPException, Depends
from fastapi import Response, Request
from sqlalchemy.ext.asyncio import AsyncSession

from application.background_tasks.send_message import (
    send_email_confirmation_code,
)
from application.core.exception.user_exception import UserNotFound, InvalidPasswordError
from application.core.models.db_helper import db_helper
from application.core.models.user import PositionType
from application.core.schemas.user import (
    SUserLog,
    SUser,
    SUserCreate,
)
from application.crud.users import add_user, get_user
from application.utils.auth_user import create_access_token
from application.utils.dependencies import authenticate_user
from application.utils.util_verification_code import (
    verification_codes,
    remove_code_after_delay,
)

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/register")
async def register_user(
    user_data: SUserCreate,
    position: PositionType,
    response: Response,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> dict:
    current_user = await get_user(session, email=user_data.email)
    if not current_user:
        # Генерация случайного 4-значного кода
        verification_code = randint(1000, 9999)
        verification_codes[user_data.email] = verification_code
        send_email_confirmation_code(user_data.email, verification_code)
        asyncio.create_task(remove_code_after_delay(user_data.email))
        data = {
            "name": user_data.name,
            "email": user_data.email,
            "password": user_data.password,
            "position": str(position.name),
        }
        response.set_cookie("user_data", json.dumps(data), httponly=True)
        return {"message": "Вам отправлен код на email"}
    else:
        return {"status": "Пользователь с таким e-mail уже существует"}


@router.post("/verify")
async def verify_register(
    code: int,
    request: Request,
    response: Response,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> SUser | dict:
    user_data_cookie = request.cookies.get("user_data")
    user_data = json.loads(user_data_cookie)
    if verification_codes[user_data["email"]] == code:
        user = await add_user(
            user_data["name"],
            PositionType[user_data["position"]],
            user_data["email"],
            user_data["password"],
            session,
        )
        response.delete_cookie("user_data", httponly=True)
        del verification_codes[user_data["email"]]
        data = SUserLog.parse_obj(
            {"email": user_data["email"], "password": user_data["password"]}
        )
        await login_user(response, data, session)
        return user
    else:
        return {"message": "Код подтверждения не верный"}


@router.post("/login")
async def login_user(
    response: Response,
    user_data: SUserLog,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    """
    Эта функция обрабатывает запрос на вход пользователя.
    Она проверяет правильность email и пароля, а затем создает и сохраняет
    JWT-токен в cookies ответа.
    """

    try:
        # Аутентифицируем пользователя по email и паролю
        user = await authenticate_user(user_data.email, user_data.password, session)

        # Создаем JWT-токен с информацией о пользователе
        access_token = create_access_token(
            {"sub": str(user.id), "admin": str(user.is_director)}
        )

        # Устанавливаем токен в cookies, делая его доступным только через HTTP
        response.set_cookie("access_token", access_token, httponly=True)

        # Возвращаем сообщение о статусе авторизации
        return {"status": "Пользователь авторизован"}

        # Обрабатываем случай, когда пользователь не найден
    except UserNotFound:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

        # Обрабатываем случай, когда пароль неверен
    except InvalidPasswordError:
        raise HTTPException(status_code=401, detail="Пароль не верный")


@router.post("/logout")
async def logout_user(response: Response) -> dict:
    """
    Эта функция обрабатывает запрос на выход пользователя.
    Она удаляет JWT-токен из cookies, тем самым деавторизуя пользователя.
    """

    # Удаляем cookie с токеном, чтобы деавторизовать пользователя
    response.delete_cookie("access_token")

    # Возвращаем сообщение о статусе деавторизации
    return {"status": "Пользователь деавторизован"}
