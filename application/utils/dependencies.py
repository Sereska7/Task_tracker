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
from application.core.models import User
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

    :param email: Email пользователя для аутентификации.
    :param password: Пароль пользователя для проверки.
    :param session: Сессия базы данных для выполнения запросов.
    :return: Возвращает объект User при успешной аутентификации.
    :raises UserNotFound: Если пользователь с указанным email не найден.
    :raises InvalidPasswordError: Если указанный пароль неверен.
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
    Функция для получения JWT-токена из запроса.

    :param request: Объект запроса, из которого будет извлечен токен.
    :return: Возвращает токен (JWT), если он присутствует в cookies или заголовках.
    """
    # Ищем токен в cookies
    token = request.cookies.get("access_token")
    if not token:
        # Если в cookies нет токена, ищем его в заголовке Authorization
        token = request.headers.get("Authorization")
        if token and token.startswith("Bearer "):
            token = token[7:]  # Убираем префикс "Bearer"
    # Возвращаем токен, если он был найден, иначе None
    return token


async def get_current_user(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    token: Optional[str] = Depends(get_token_from_request),
) -> Optional[User]:
    """
    Получение текущего пользователя на основе JWT-токена.

    :param request: Объект запроса, из которого будет извлечен токен.
    :param session: Сессия базы данных для выполнения запросов.
    :param token: JWT-токен для декодирования пользователя (может быть None).
    :return: Возвращает объект User, если токен валиден, иначе None для неавторизованных.
    :raises HTTPException: Если токен некорректный или пользователь не найден.
    """
    # Если токен отсутствует, пользователь не авторизован
    if not token:
        return None  # Вернем None для неавторизованных пользователей

    try:
        # Раскодируем токен с использованием секретного ключа и алгоритма
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Ошибка проверки токена.")

    # Извлекаем идентификатор пользователя из payload токена
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Некорректный токен.")

    # Ищем пользователя в базе данных по идентификатору
    user = await get_user(session, id=int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")

    # Возвращаем объект пользователя
    return user

