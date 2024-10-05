import json
from random import randint
from typing import Annotated, Dict

import asyncio
from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi import Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse, JSONResponse

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
    SUserCreateForm,
    SUserLogForm,
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
    user_data: Annotated[SUserCreateForm, Depends(SUserCreateForm.as_form)],
    response: Response,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> dict:
    current_user = await get_user(session, email=user_data.email)
    if not current_user:
        verification_code = randint(1000, 9999)
        verification_codes[user_data.email] = verification_code
        send_email_confirmation_code(user_data.email, verification_code)
        asyncio.create_task(remove_code_after_delay(user_data.email))

        data = {
            "name": user_data.name,
            "email": user_data.email,
            "password": user_data.password,
            "position": str(user_data.position.name),
        }

        response.set_cookie(
            key="user_data",
            value=json.dumps(data),
            httponly=True,
            path="/",
            samesite="Lax",
            secure=False,
        )
        return RedirectResponse(
            url="/pages/verify", status_code=303, headers=dict(response.headers)
        )
    else:
        return {"status": "Пользователь с таким e-mail уже существует"}


@router.post("/verify")
async def verify_register(
    request: Request,
    response: Response,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    code: int = Form(...),
) -> SUser | dict:
    # Чтение cookies
    user_data_cookie = request.cookies.get("user_data")

    # Отладка чтения cookies
    print(f"Cookies получены: {user_data_cookie}")
    response = RedirectResponse(url="/pages/base", status_code=303)
    response.delete_cookie("user_data", httponly=True)
    if not user_data_cookie:
        return JSONResponse(
            status_code=400, content={"message": "Данные пользователя не найдены"}
        )

    user_data = json.loads(user_data_cookie)
    if verification_codes.get(user_data["email"]) == code:
        user = await add_user(
            name=user_data["name"],
            position=PositionType(user_data["position"].title()),
            email=user_data["email"],
            password=user_data["password"],
            session=session,
        )
        # Аутентифицируем пользователя по email и паролю
        current_user = await authenticate_user(
            user_data["email"], user_data["password"], session
        )
        # Создаем JWT-токен с информацией о пользователе
        access_token = create_access_token(
            {"sub": str(current_user.id), "admin": str(current_user.is_director)}
        )
        # Устанавливаем токен в cookies, делая его доступным только через HTTP
        response.set_cookie(
            "access_token",
            access_token,
            httponly=True,
        )
        del verification_codes[user_data["email"]]
        return response
    else:
        return JSONResponse(
            status_code=400, content={"message": "Код подтверждения неверен"}
        )


@router.post("/login")
async def login_user(
    response: Response,
    user_data: Annotated[SUserLogForm, Depends(SUserLogForm.as_form)],
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
        response.set_cookie(
            "access_token",
            access_token,
            httponly=True,
        )

        # Возвращаем сообщение о статусе авторизации
        return RedirectResponse(
            url="/pages/base", status_code=303, headers=dict(response.headers)
        )

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
    response = RedirectResponse(url="/pages/base", status_code=303)
    response.delete_cookie("access_token", httponly=True)

    # Возвращаем сообщение о статусе деавторизации
    return response
