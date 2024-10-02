from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.exception.user_exception import UserNotFound, InvalidPasswordError
from application.core.models.db_helper import db_helper
from application.core.models.user import PositionType
from application.core.schemas.user import SUserLog, SUser, SUserCreate
from application.crud.users import create_user
from application.utils.auth_user import create_access_token
from application.utils.dependencies import authenticate_user

router = APIRouter(
    tags=["Auth"],
    prefix="/auth"
)


@router.post("/register")
async def register_user(
        user_data: SUserCreate,
        position: PositionType,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ]
) -> SUser:
    user = await create_user(
        position,
        user_data,
        session
    )
    return user


@router.post("/login")
async def login_user(
        response: Response,
        user_data: SUserLog,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ]
):
    """
        Эта функция обрабатывает запрос на вход пользователя.
        Она проверяет правильность email и пароля, а затем создает и сохраняет
        JWT-токен в cookies ответа.
        """

    try:
        # Аутентифицируем пользователя по email и паролю
        user = await authenticate_user(
            user_data.email,
            user_data.password,
            session
        )

        # Создаем JWT-токен с информацией о пользователе
        access_token = create_access_token({"sub": str(user.id)})

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
