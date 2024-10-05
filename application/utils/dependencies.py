from typing import Annotated, Optional

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


async def get_token_from_request(request: Request) -> Optional[str]:
    """
    Функция для получения JWT-токена из запроса. Токен может быть необязательным.
    """
    token = request.cookies.get("access_token")
    if not token:
        token = request.headers.get("Authorization")
        if token and token.startswith("Bearer "):
            token = token[7:]
    return token  # Если токен не найден, возвращаем None


async def get_current_user(
        request: Request,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        token: Optional[str] = Depends(get_token_from_request)
):
    # Если токен отсутствует, пользователь не авторизован
    if not token:
        return None  # Вернем None для неавторизованных пользователей

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Ошибка проверки токена.")

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Некорректный токен.")

    user = await get_user(session, id=int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")

    return user
