from typing import Annotated

from fastapi import HTTPException, Depends, Request
from jose import jwt, ExpiredSignatureError, JWTError
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.config import settings
from application.core.exception.user_exception import (
    TokenNotFound,
    InvalidPasswordError,
    UserNotFound,
)
from application.core.models.db_helper import db_helper
from application.crud.users import get_user
from application.utils.auth_user import verify_password


async def authenticate_user(
    email: EmailStr,
    password: str,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    """
    Аутентификация пользователя.

    Проверяет наличие пользователя с указанным email и соответствие пароля.
    """

    # Ищем пользователя по email в базе данных
    user = await get_user(session, email=email)

    # Если пользователь не найден, выбрасываем исключение UserNotFound
    if not user:
        raise UserNotFound
    else:
        # Проверяем соответствие переданного пароля хэшированному паролю пользователя
        if not verify_password(password, user.hash_password):
            # Если пароли не совпадают, выбрасываем исключение InvalidPasswordError
            raise InvalidPasswordError

    # Возвращаем объект пользователя, если аутентификация успешна
    return user


def get_token(request: Request):
    """Извлечение токена из cookies запроса."""

    # Извлечение токена из cookies с ключом "access_token"
    token = request.cookies.get("access_token")

    # Если токен отсутствует, выбрасываем исключение с кодом 404
    if not token:
        raise HTTPException(status_code=404, detail="Пользователь не аутентифицирован")

    # Возвращаем извлеченный токен
    return token


async def get_current_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    token: str = Depends(get_token),
):
    """
    Получает текущего пользователя по JWT-токену.

    Декодирует токен, проверяет его валидность и извлекает ID пользователя.
    Если токен недействителен или пользователь не найден, выбрасывает HTTPException.
    """
    try:
        # Декодируем токен с использованием секретного ключа и алгоритма
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)

        # Обработка случаев, когда токен не найден
    except TokenNotFound:
        raise HTTPException(status_code=404, detail="Токен пользователя не найден")

        # Обработка случаев, когда срок действия токена истек
    except ExpiredSignatureError:
        raise HTTPException(status_code=500, detail="Срок действия токена истек.")

        # Обработка других ошибок при работе с JWT
    except JWTError:
        raise HTTPException(status_code=401, detail="Произошла непредвиденная ошибка.")

        # Извлекаем идентификатор пользователя из payload и ищем пользователя в базе данных
    user = await get_user(session, id=int(payload.get("sub")))

    # Если пользователь не найден, возвращаем ошибку 404
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")

    # Возвращаем объект пользователя
    return user
