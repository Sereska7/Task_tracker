import json
from random import randint
from typing import Annotated, Dict

import asyncio
from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi import Response, Request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse, JSONResponse

from application.background_tasks.send_message import (
    send_email_confirmation_code,
)
from application.core.exception.user_exception import UserNotFound, InvalidPasswordError
from application.core.models.db_helper import db_helper
from application.core.models.user import PositionType
from application.core.schemas.user import (
    SUser,
    SUserCreateForm,
    SUserLogForm,
)
from application.crud.users import add_user, get_user
from application.utils.auth_user import create_access_token
from application.utils.dependencies import authenticate_user
from application.utils.verification_code import (
    verification_codes,
    remove_code_after_delay,
)

# Роутер для обработки авторизации и регистрации
router = APIRouter(tags=["Auth"], prefix="/auth")


# Регистрация пользователя
@router.post("/register")
async def register_user(
    user_data: Annotated[
        SUserCreateForm, Depends(SUserCreateForm.as_form)
    ],  # Зависимость формы для сбора данных
    response: Response,  # Ответ для задания cookies
    session: Annotated[
        AsyncSession, Depends(db_helper.session_getter)
    ],  # Получение сессии БД
) -> dict:
    """
    Регистрация нового пользователя:
    - Проверяет, существует ли пользователь с данным email.
    - Если пользователя нет, отправляет код подтверждения на email.
    - Временные данные сохраняются в cookies до подтверждения.
    """
    try:
        current_user = await get_user(
            session, email=user_data.email
        )  # Проверка на существование пользователя
        if not current_user:
            # Генерация и отправка кода подтверждения
            verification_code = randint(1000, 9999)
            verification_codes[user_data.email] = verification_code
            send_email_confirmation_code(user_data.email, verification_code)
            asyncio.create_task(remove_code_after_delay(user_data.email))

            # Сохранение временных данных пользователя в cookies
            data = {
                "name": user_data.name,
                "email": user_data.email,
                "password": user_data.password,
                "position": str(user_data.position.name),
            }

            # Установка cookies с данными
            response.set_cookie(
                key="user_data",
                value=json.dumps(data),
                httponly=True,
                path="/",
                samesite="Lax",
                secure=False,
            )

            # Перенаправление на страницу подтверждения
            return RedirectResponse(
                url="/pages/verify", status_code=303, headers=dict(response.headers)
            )
        else:
            return {"status": "Пользователь с таким e-mail уже существует"}

    # Обработка ошибок базы данных
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Ошибка базы данных") from e

    # Обработка ошибок валидации
    except ValidationError as e:
        raise HTTPException(
            status_code=400, detail="Ошибка валидации данных пользователя"
        ) from e

    # Обработка любых других ошибок
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Произошла неизвестная ошибка"
        ) from e


# Подтверждение регистрации
@router.post("/verify")
async def verify_register(
    request: Request,  # Запрос для получения cookies
    session: Annotated[
        AsyncSession, Depends(db_helper.session_getter)
    ],  # Получение сессии БД
    code: int = Form(...),  # Код подтверждения из формы
) -> SUser | dict:
    """
    Подтверждение регистрации:
    - Проверяет код подтверждения, сохраненный в cookies.
    - Создает пользователя в базе данных, если код подтвержден.
    """
    try:
        # Чтение cookies с данными пользователя
        user_data_cookie = request.cookies.get("user_data")

        # Удаление cookies с данными пользователя
        response = RedirectResponse(url="/pages/base", status_code=303)
        response.delete_cookie("user_data", httponly=True)

        # Если данные не найдены в cookies
        if not user_data_cookie:
            return JSONResponse(
                status_code=400, content={"message": "Данные пользователя не найдены"}
            )

        # Декодируем данные пользователя из cookies
        user_data = json.loads(user_data_cookie)

        # Проверка правильности кода подтверждения
        if verification_codes.get(user_data["email"]) == code:
            # Создание пользователя
            user = await add_user(
                name=user_data["name"],
                position=PositionType(user_data["position"].title()),
                email=user_data["email"],
                password=user_data["password"],
                session=session,
            )

            # Аутентификация и генерация токена
            current_user = await authenticate_user(
                user_data["email"], user_data["password"], session
            )

            # Создание JWT-токена
            access_token = create_access_token(
                {"sub": str(current_user.id), "admin": str(current_user.is_director)}
            )

            # Установка токена в cookies
            response.set_cookie("access_token", access_token, httponly=True, path="/")

            # Удаление кода подтверждения
            del verification_codes[user_data["email"]]

            # Удаление cookies с данными пользователя
            response.delete_cookie("user_data", httponly=True)

            # Перенаправление на главную страницу
            return RedirectResponse(url="/pages/base", status_code=303)
        else:
            return JSONResponse(
                status_code=400, content={"message": "Код подтверждения неверен"}
            )

    # Обработка ошибок базы данных
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Ошибка базы данных") from e

    # Обработка любых других ошибок
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Произошла неизвестная ошибка"
        ) from e


# Вход пользователя
@router.post("/login")
async def login_user(
    user_data: Annotated[
        SUserLogForm, Depends(SUserLogForm.as_form)
    ],  # Зависимость формы для получения данных
    session: Annotated[
        AsyncSession, Depends(db_helper.session_getter)
    ],  # Получение сессии БД
):
    """
    Авторизация пользователя:
    - Проверяет правильность введенных email и пароля.
    - После успешной авторизации сохраняет JWT-токен в cookies.
    """
    try:
        # Аутентификация пользователя по email и паролю
        user = await authenticate_user(user_data.email, user_data.password, session)

        # Генерация JWT-токена
        access_token = create_access_token(
            {"sub": str(user.id), "admin": str(user.is_director)}
        )

        # Установка токена в cookies
        response = RedirectResponse(url="/pages/base", status_code=303)
        response.set_cookie("access_token", access_token, httponly=True)

        # Перенаправление на главную страницу
        return response

    # Исключение: Пользователь не найден
    except UserNotFound:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Исключение: Неверный пароль
    except InvalidPasswordError:
        raise HTTPException(status_code=401, detail="Пароль неверный")

    # Обработка ошибок базы данных
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Ошибка базы данных") from e

    # Обработка любых других ошибок
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Произошла неизвестная ошибка"
        ) from e


# Выход пользователя
@router.post("/logout")
async def logout_user(response: Response) -> dict:
    """
    Выход пользователя:
    - Удаляет JWT-токен из cookies, деавторизуя пользователя.
    """
    try:
        # Удаление токена из cookies
        response = RedirectResponse(url="/pages/base", status_code=303)
        response.delete_cookie("access_token", httponly=True)

        # Перенаправление на главную страницу
        return response

    # Обработка любых других ошибок
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Произошла неизвестная ошибка"
        ) from e
