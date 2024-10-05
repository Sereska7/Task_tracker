from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from application.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Возвращает хеш пароля с использованием bcrypt.
    """
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    """
    Проверяет соответствие открытого пароля и хешированного пароля.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    Создание JWT токена для авторизации пользователя.
    """
    # Создаем копию переданных данных для кодирования
    to_encode = data.copy()

    # Кодируем данные в JWT токен, используя секретный ключ и алгоритм
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)

    # Возвращаем закодированный JWT токен
    return encoded_jwt
